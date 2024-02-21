const defaultMetadata = require('../models/defaultMetadata');
const createdefaultMetadata = require('../gamer/createdefaultMetadata');

async function listAllMetadataController(req, res) {
    try {
        const data = await defaultMetadata.find({});
        res.render('metadata', { data });

    } catch (error) {

        res.status(500).send(error);
    }
};

async function getMetadataByIdController(req, res) {
    try {
        const data = await defaultMetadata.findById(req.params.id);
        
        if(data == null){
            console.log("File metadata not found");
            return res.status(404).send('File metadata was not found');
        }
        res.render('metadata', { data });

    } catch (error) {

        res.status(500).send(error);
    }   
}

async function addMetadataController(req, res) {
    try {

        const { name, creationDT, lastModifiedDT, lastAccessedDT, size, description } = req.body;


        const newMetadata = new defaultMetadata({
            name: name,
            creationDT: creationDT,
            lastModifiedDT: lastModifiedDT,
            lastAccessedDT: lastAccessedDT,
            size: size,
            description: description,
        })

        await newMetadata.save();

        res.redirect('/md/list');

    } catch (error) {

        res.status(500).send(error);
    }
}

async function updateMetadataByIdController(req, res) {
    const id = req.params.id;
    const { name, creationDT, lastModifiedDT, lastAccessedDT, size, description } = req.body;

    try {
        const updatedMetadata = await defaultMetadata.findByIdAndUpdate( id, { name, creationDT, lastModifiedDT, lastAccessedDT, size, description });

        if (!updatedMetadata) {
            return res.status(404).send('Metadata not found with the specified ID');
        }

        res.status(200).send();

    } catch (error) {
        console.error(error);
        res.status(500).send(error);
    }
}

async function deleteMetadataByIdController(req, res) {
    const id = req.params.id;

    try {
        const result = await defaultMetadata.findByIdAndDelete(id);

        if (!result) {
            return res.status(404).send('Metadata not found with the specified ID');
        }

        res.status(200).send('bing bong metadata gone');

    } catch (error) {
        console.error(error);
        res.status(500).send(error);
    }
}

module.exports = {
    getMetadataByIdController,
    listAllMetadataController,
    addMetadataController,
    updateMetadataByIdController,
    deleteMetadataByIdController,
}