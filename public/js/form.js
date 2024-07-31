const form = document.querySelector('#inputform');
const downloadBtn = document.querySelector('#download');

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
        const outputHtml = `
        Sign Bit: ${data.output.sign_bit} <br>
        Combination Field: ${data.output.combination_bit} <br>
        Exponent Field: ${data.output.exponent_bit} <br>
        Significand Field: ${data.output.first_significand_bit} ${data.output.second_significand_bit} <br>
        Binary: ${data.output.binary_output} <br>
        Hex: ${data.output.hex_output.toUpperCase()} <br>
        `;
        document.querySelector('#output').innerHTML = outputHtml;
        downloadBtn.style.display = 'block';
        downloadBtn.addEventListener('click', () => downloadOutput(data.output));
    } catch(err){
        console.log('error', err);
        alert('error occured', err);

    }
});


function downloadOutput(output){
    const formattedOutput = `
    Sign Bit: ${output.sign_bit}
    Combination Field: ${output.combination_bit}
    Exponent Field: ${output.exponent_bit}
    Significand Field: ${output.first_significand_bit} ${output.second_significand_bit}
    Binary: ${output.binary_output}
    Hex: ${output.hex_output.toUpperCase()}
    `;

    const blob = new Blob([formattedOutput], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href= url;
    a.download = 'output.txt';
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}