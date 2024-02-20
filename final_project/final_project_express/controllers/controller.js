const defaultMetadata = require('../models/defaultMetadata');
const createdefaultMetadata = require('../gamer/createdefaultMetadata');

async function listAllMetadataController(req, res) {
    try {
        const mdObjects = await defaultMetadata.find({});
        console.log(mdObjects);
        res.status(200).send("it workey");

    } catch (error) {

        res.status(500).send(error);
    }
};

async function getMetadataByIdController(req, res) {
    try {
        const metadata = await defaultMetadata.findById(req.params.id);
        
        if(metadata == null){
            console.log("File metadata not found");
            return res.status(404).send('File metadata was not found');
        }
        console.log(metadata)
        res.status(200).send("it workey");

    } catch (error) {

        res.status(500).send(error);
    }   
}

module.exports = {
    getMetadataByIdController,
    listAllMetadataController
}