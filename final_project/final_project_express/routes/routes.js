const express = require('express');
const router = express.Router();
const controller = require('../controllers/controller');


router.put('/new', controller.addMetadataController);
router.get('/list', controller.listAllMetadataController);
router.put('/update/:id', controller.updateMetadataByIdController);
router.get('/get/:id', controller.getMetadataByIdController);
router.delete('/delete/:id', controller.deleteMetadataByIdController);

module.exports = router;