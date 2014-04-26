<?php
require_once '../lib/util.inc';

require_once './insertCard_model.inc';

$model = new insertCard_model();

$model->getForm();

$model->processing();

require_once './insertCard.phtml';
?>