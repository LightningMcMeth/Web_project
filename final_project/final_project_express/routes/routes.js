const express = require('express');
const router = express.Router();
const controller = require('../controllers/controller');


router.put('/new', controller.addMetadataController);
router.get('/list', controller.listAllMetadataController);
router.put('/update/:id', controller.updateMetadataByIdController);
router.put('/updateByName/:name', controller.updateMetadataByNameController)
router.get('/get/:id', controller.getMetadataByIdController);
router.delete('/delete/:id', controller.deleteMetadataByIdController);
router.delete('/deleteByName/:name', controller.deleteMetadataByNameController);
router.get('/getByName/:name', controller.getMetadataByNameController);

module.exports = router;