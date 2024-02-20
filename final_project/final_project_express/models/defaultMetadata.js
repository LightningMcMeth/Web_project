const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const defaultMetadataSchema = new Schema({

    name: String,
    creationDT: Date,
    lastModifiedDT: Date,
    lastAccessedDT: Date,
    size: Number,
    description: String,

})

const defaultMetadata = mongoose.model('defaultMetadata', defaultMetadataSchema);

module.exports = defaultMetadata;