const form = document.getElementById('inputform');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const decimal = document.querySelector('#decimal_input').value;
    const exponent = document.querySelector('#exponent_input').value;
    const rnd_methd = document.querySelector('input[name="rnd_mthd"]:checked').value;
    console.log(decimal, exponent);

    const jstring = JSON.stringify({
        decimal,
        exponent,
        rnd_methd
    });

    try{
        const res = await fetch('/', {
            method: 'POST',
            body: jstring,
            headers: {
                'content-type': 'application/json'
            }
        });
        const data = await res.json();
        document.querySelector('#output').innerHTML = data.output;
    } catch(err){
        console.log('error', err);
        alert('error occured', err);

    }
});