// static/script.js
/*document.addEventListener('DOMContentLoaded', function() {
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
});*/

// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Registrar presença
    const presencaForm = document.getElementById('presencaForm');
    
    if (presencaForm) {
        presencaForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(presencaForm);
            const data = {
                membro_id: formData.get('membro_id'),
                evento_id: formData.get('evento_id'),
                presente: formData.get('presente')
            };
            
            try {
                const response = await fetch('/registrar_presenca', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNotification('Presença registrada com sucesso!', 'success');
                    presencaForm.reset();
                } else {
                    throw new Error('Erro ao registrar presença');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Ocorreu um erro ao registrar a presença.', 'error');
            }
        });
    }
});

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}