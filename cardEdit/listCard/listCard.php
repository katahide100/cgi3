<?php
require_once './listCard_model.inc';

$model = new listCard_model();

//$model->getForm();

$model->processing();

require_once './listCard.phtml';

?>