// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const presencaForm = document.getElementById('presencaForm');
    
    if (presencaForm) {
        presencaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(presencaForm);
            const data = {
                membro_id: formData.get('membro_id'),
                evento_id: formData.get('evento_id'),
                presente: formData.get('presente')
            };
            
            fetch('/registrar_presenca', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Presença registrada com sucesso!');
                    presencaForm.reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao registrar a presença.');
            });
        });
    }
});