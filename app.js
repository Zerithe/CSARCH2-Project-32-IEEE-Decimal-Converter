import express from 'express';
import { engine } from 'express-handlebars';
import 'dotenv/config';
import bodyParser from 'body-parser';
import { exec } from 'child_process';

const app = express();

app.use(express.static('.\\views'));
app.use(bodyParser.json());
app.use('/static', express.static('public'));

app.engine('handlebars', engine());
app.set('view engine', 'handlebars');
app.set('views', '.\\views');

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
    exec(`py test.py`, (error, stdout, stderr) => {
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
    if(inputValidation(decimal, exponent)){
        console.log('valid input');
        //replace with python exec later
        exec(`py decimal_to_ieee.py ${decimal} ${exponent} ${rnd_methd}`, (error, stdout, stderr) => {
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
    } else {
        console.log('invalid input');
        res.json({output: 'Invalid Input'});
    }

});

app.listen(process.env.SERVER_PORT, () => {
    console.log('server is now listening...');
});