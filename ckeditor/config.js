/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	//config.width=600;
	config.height=350;
	config.basicEntities = false;
	config.entities = false;
	config.allowedContent = true;
	//config.fullPage = true;
	config.contentsCss = '../../css/help.css';
	config.filebrowserImageBrowseUrl = '../../kcfinder/browse.php?type=images';
    config.filebrowserImageUploadUrl = '../../kcfinder/upload.php?type=images';
};
