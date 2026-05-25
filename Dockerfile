FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Apache + Perl + PHP + cron + tools
RUN apt-get update && apt-get install -y \
    apache2 \
    perl \
    libcgi-pm-perl \
    libnet-ssleay-perl \
    libwww-perl \
    libhttp-message-perl \
    libjson-perl \
    php \
    php-mbstring \
    php-xml \
    php-gd \
    php-pdo \
    php-mysqlnd \
    php-json \
    php-curl \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Perl wrapper to match shebang (#!/usr/local/bin/perl) with UTF-8 source support
RUN echo '#!/bin/sh' > /usr/local/bin/perl && \
    echo 'exec /usr/bin/perl -Mutf8 "$@"' >> /usr/local/bin/perl && \
    chmod +x /usr/local/bin/perl

# Install Node.js 16.x
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Enable Apache modules
RUN a2enmod cgid && a2enmod rewrite && a2enmod php8.1

# Apache CGI config
COPY docker/apache-cgi3.conf /etc/apache2/conf-available/cgi3.conf
RUN a2enconf cgi3

# App directory
WORKDIR /var/www/html/cgi3
COPY . .

# Add 'use utf8;' and 'use open ":std", ":utf8";' to all Perl files
# (source files contain UTF-8 Japanese characters; file I/O uses UTF-8 data files)
RUN find /var/www/html/cgi3 \( -name "*.cgi" -o -name "*.pl" \) \
    ! -path "*/ckeditor/*" ! -path "*/kcfinder/*" \
    ! -name "jcode.pl" \
    -exec sed -i '2i use open ":std", ":utf8";' {} \; \
    -exec sed -i '1a use utf8;' {} \;

# Install Node.js dependencies
RUN npm install --production

# Setup
RUN mkdir -p /var/www/html/cgi3/logs && chmod 777 /var/www/html/cgi3/logs
RUN cp -n cust.default.cgi cust.cgi || true

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80 3002

ENTRYPOINT ["/entrypoint.sh"]
