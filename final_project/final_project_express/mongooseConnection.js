const mongoose = require('mongoose');
const mongoConnection = require('./configs/mongoConnection');
const defaultMetadata = require('./models/defaultMetadata');


mongoose.connect(mongoConnection);

const connection = mongoose.connection;

connection.on('error', () => console.log('mongodb no workey :('));
connection.once('open', () => console.log('connected to mongodb'));

module.exports = mongoose;