const defaultMetadata = require('../models/defaultMetadata');

function createDefaultMetadata(name, creationDT, lastModifiedDT, lastAccessedDT, size, description, metadata) {

    const defaultMD = new DefaultMetadata({
        name: name,
        creationDT: creationDT,
        lastModifiedDT: lastModifiedDT,
        lastAccessedDT: lastAccessedDT,
        size: size,
        description: description,
    })

    return defaultMD.save();
}

module.exports = {
    createDefaultMetadata
}