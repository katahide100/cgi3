<?php
require_once '../lib/util.inc';

require_once './deleteCard_model.inc';

$model = new deleteCard_model();

$model->getForm();

$model->processing();

require_once './deleteCard.phtml';
?>