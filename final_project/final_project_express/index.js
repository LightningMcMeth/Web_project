const express = require('express');
const bodyParser = require('body-parser');
const PORT = require('./configs/port');
const mongoose = require('./mongooseConnection');
const routes = require('./routes/routes');
const cors = require('cors');
const morgan = require('morgan');
const fs = require('fs');

const app = express();

const logDir = './logs';
const logFile = fs.createWriteStream(`${logDir}/access.log`, { flags: 'a' });
const logErrorFile = fs.createWriteStream(`${logDir}/errors.log`, { flags: 'a' });

app.use(morgan('common', { stream: logFile }));
app.use(morgan('common', { stream: logErrorFile, skip: function (req, res) { return res.statusCode < 400 }  }));


const whitelist = ["http://localhost:8000"];
const corsOptions = {
    origin: originFunction,
};

function originFunction(origin, callback) {

    if (whitelist.includes(origin) || !origin) {

        callback(null, true);
    } else {

        callback(new Error("Not allowed by CORS"));
    }
}
app.use(cors(corsOptions));
//app.use(cors({ origin: false }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());
app.set('view engine', 'pug');
app.set('views', 'views');

app.use('/md', routes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
