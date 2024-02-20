const express = require('express');
const router = express.Router();
const controller = require('../controllers/controller');


//router.get('/new', controller.addMetadataController);
router.get('/listmd', controller.listAllMetadataController);
router.get('/:id', controller.getMetadataByIdController);

module.exports = router;