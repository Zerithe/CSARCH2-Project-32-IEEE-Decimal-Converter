import express from 'express';
import { engine } from 'express-handlebars';
import 'dotenv/config';
import bodyParser from 'body-parser';
import { exec } from 'child_process';

const app = express();

app.use(express.static('views'));
app.use(bodyParser.json());

app.engine('handlebars', engine());
app.set('view engine', 'handlebars');
app.set('views', '.\\views');

app.get('/', function(req, res){
    exec(`py test.py`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
        }

        if (stderr) {
            console.error(`stderr: ${stderr}`);
        }
        console.log(stdout.trim());
    });
    res.render('test');
});

app.listen(process.env.SERVER_PORT, () => {
    console.log('server is now listening...');
});