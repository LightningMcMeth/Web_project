const express = require('express');
const bodyParser = require('body-parser');
const PORT = require('./configs/port');
const mongoose = require('./mongooseConnection');
const routes = require('./routes/routes');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());
app.set('view engine', 'pug');
app.set('views', 'views');


app.use('/md', routes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
