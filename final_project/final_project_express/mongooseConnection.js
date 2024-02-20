const mongoose = require('mongoose');
const mongoConnection = require('./configs/mongoConnection');
const defaultMetadata = require('./models/defaultMetadata');


mongoose.connect(mongoConnection);

const connection = mongoose.connection;

connection.on('error', () => console.log('mongodb no workey :('));
connection.once('open', () => console.log('connected to mongodb'));

const dummyData = [
    {
        name: 'Example File 1',
        creationDT: new Date(),
        lastModifiedDT: new Date(),
        lastAccessedDT: new Date(),
        size: 1024,
        description: 'This is a dummy file description for file 1.'
    },
    {
        name: 'Example File 2',
        creationDT: new Date(),
        lastModifiedDT: new Date(),
        lastAccessedDT: new Date(),
        size: 2048,
        description: 'This is a dummy file description for file 2.'
    }
];

defaultMetadata.insertMany(dummyData)
    .then(() => {
        console.log('Dummy data inserted successfully!');
        mongoose.connection.close();
    })
    .catch((error) => {
        console.error('Error inserting dummy data:', error);
        mongoose.connection.close();
    });


module.exports = mongoose;