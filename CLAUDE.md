# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

デュエル・マスターズ対戦CGI — a web-based TCG battle system built as Perl CGI scripts with a Node.js WebSocket server for real-time duel actions.

### Entry points and their roles

| Script | Role |
|---|---|
| `index.cgi` | Top page: login, user registration, navigation |
| `taisen.cgi` | Room list / matchmaking — enter/leave duel rooms |
| `duel.cgi` + `common.pl` | The duel game engine (card battle logic, phases, effects) |
| `deck.cgi` | Deck builder / editor |
| `admin.cgi` / `admin_d.cgi` | Admin panel |

### Shared modules

- **`duel.pl`** (496 lines) — Required by nearly all .cgi scripts. Provides: HTML generation (`header`, `footer`), user profile I/O (`pfl_read`/`pfl_write`), password/auth, file locking, opponent lookup (`prof`), cookie handling, and chat server API calls.
- **`common.pl`** (1539 lines) — Required only by `duel.cgi` and `duelold.cgi`. The core duel engine: battle zone management, phase transitions, combat resolution, card effects.
- **`cust.cgi`** — Config file generated from `cust.default.cgi`. Contains server paths, hostnames, ports, admin password, feature flags.
- **`jcode.pl`** — Japanese character encoding conversion library (EUC-JP/SJIS/UTF-8).

### Real-time communication

- **`app_node.js`** — Socket.IO v1 server on port 3002. Relays duel actions (`action` events) and chat messages between players in the same room. Falls back to HTTP if SSL certs are unavailable (Docker/local dev).
- **`logger.js`** — Log4js-based request logger for the Node.js server.
- Client-side: `duel.cgi` and `duelold.cgi` load socket.io.js from `$hostName:$nodePort` and connect via `io.connect()`.

### External dependencies

- **Chat server** (port 1337) — Separate service at `$chatNodeHost`. Used for user sync (find/update/create) and orica flag lookup. Calls are wrapped in `eval {}` so connection failures are non-fatal.

### Data storage

All data is flat-file based under these directories:
- `playerdata/` — One `.cgi` file per user (tab-separated key=value)
- `room/` — Room state files for active duels
- `data/` — Game data: `dendou.txt` (hall of fame cards), `premium.txt` (premium hall of fame)
- `card1.txt`, `card2.txt`, `syu.txt` — Card database
- `deck.dat` — Deck definitions
- `taikai/` — Tournament data
- `chat/data/` — Chat logs
- `lock/` — Lock files for concurrency control

### Configuration

On first run, copy `cust.default.cgi` → `cust.cgi` and edit it. Key settings:
- `$hostName` — Base URL (used for socket.io client connection)
- `$nodePort` — Port 3002 (duel WebSocket)
- `$chatNodePort` — Port 1337 (external chat server)
- `$admin` — Admin password
- `$player_dir`, `$room_dir` — Data directory paths

PHP auxiliary files (`base.php`, `dl.php`, `dl_form.php`, etc.) share config via `config/define.php`.

## Running

### With Docker

```bash
docker-compose up -d
# → http://localhost:8080/cgi3/index.cgi
```

### On existing Apache (production)

Per README.md: requires Apache with `Options +ExecCGI` and `AddHandler cgi-script .cgi .pl`, Perl with CPAN modules (Net::SSLeay, LWP::UserAgent, HTTP::Request::Common, JSON), PHP with mbstring/xml/gd/pdo extensions, and Node.js for `app_node.js` (started via `forever start app_node.js`).

Perl shebangs expect `#!/usr/local/bin/perl`. On Ubuntu, create a symlink: `ln -s /usr/bin/perl /usr/local/bin/perl`.

Source files contain UTF-8 Japanese characters in comments/strings. The Dockerfile adds `use utf8;` to all `.cgi`/`.pl` files at build time. For bare-metal Apache, ensure Perl parses source as UTF-8 (via `-Mutf8` flag or `use utf8;` in files with non-ASCII characters).

## Encoding

Source files are UTF-8 (originally EUC-JP). HTML meta tags declare `charset=utf-8`. The `jcode.pl` library handles encoding conversion for legacy card data.

## Cron jobs

Per README, four cron entries are needed:
```
* * * * * roomreset.sh              # Clean empty rooms
* * * * * script/permission_reset.sh # Reset file permissions
0 0 * * * script/logreset.sh         # Rotate request.log
0 0 * * 0 script/populerreset.sh     # Reset popularity counter
```

In Docker, these are set up automatically by `docker/entrypoint.sh`.
