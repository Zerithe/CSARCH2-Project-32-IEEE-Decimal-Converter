import express from 'express';
import { engine } from 'express-handlebars';
import 'dotenv/config';
import bodyParser from 'body-parser';
import { exec } from 'child_process';
import path from 'path';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const app = express(); 
const port = process.env.PORT || 3000;

const __dirname = dirname(fileURLToPath(import.meta.url));

app.use(express.static(path.join(__dirname, 'views')));
app.use(bodyParser.json());
app.use('/static', express.static(path.join(__dirname, 'public')));

app.engine('handlebars', engine());
app.set('view engine', 'handlebars');
app.set('views', path.join(__dirname, 'views'));

function inputValidation(decimal, exponent_input){
    var regExp = /^[+-]?[0-9.]+$/;
    var regExpExponent = /^[+-]?[0-9]+$/;
    if(regExp.test(decimal) && regExpExponent.test(exponent_input)){
        return true;
    } else {
        return false;
    }
}

app.get('/', (req, res) => {
    exec(`python test.py`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
        }

        if (stderr) {
            console.error(`stderr: ${stderr}`);
        }
        console.log(stdout.trim());
    });
    res.render('form');
});

app.post('/', async (req, res) => {
    console.log(req.body);
    const {decimal, exponent, rnd_methd} = req.body;
    console.log(decimal, ' ', exponent, ' ', rnd_methd);
    exec(`python decimal_to_ieee.py ${decimal} ${exponent} ${rnd_methd}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
        }

        if (stderr) {
            console.error(`stderr: ${stderr}`);
        }
        console.log(stdout.trim());
        try{
            const output = JSON.parse(stdout.trim());
            res.json({output});
        } catch (err) {
            console.error('JSON parse error: ', err);
            res.status(500).json({output: 'Internal Server Error'});
        }
    });
});

app.listen(port, () => {
    console.log('server is now listening...');
});