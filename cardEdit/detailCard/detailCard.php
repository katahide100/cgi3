<?php
require_once '../lib/util.inc';

require_once './detailCard_model.inc';

$model = new detailCard_model();

$model->getForm();

$model->processing();

require_once './detailCard.phtml';
?>