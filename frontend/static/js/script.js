// Configuração da API
const API_BASE_URL = window.location.origin;

// Conjunto de carrinhos selecionados
let selectedCarts = new Set();

// Helper para obter token de autenticação
function getAuthToken() {
    return sessionStorage.getItem('access_token') || 
           localStorage.getItem('access_token') ||
           document.querySelector('meta[name="token"]')?.getAttribute('content');
}

// Selecionar / desselecionar carrinho
function toggleSelect(cartId, cartName) {
    const card = document.getElementById(`cart-${cartId}`);
    const dot = document.getElementById(`dot-${cartId}`);
    const manageContainer = document.getElementById("manage-container");

    if (selectedCarts.has(cartId)) {
        selectedCarts.delete(cartId);
        card.classList.remove('selected');
        dot.classList.remove('active');
        const box = document.getElementById(`manage-${cartId}`);
        if (box) box.remove();
    } else {
        selectedCarts.add(cartId);
        card.classList.add('selected');
        dot.classList.add('active');

        const box = document.createElement("div");
        box.className = "manage-cart";
        box.id = `manage-${cartId}`;
        box.innerHTML = `
            <h2>Gerenciar Carrinho: ${cartName}</h2>
            <form action="/add_to_cart/${cartId}" method="post" class="add-form compact">
                <input type="text" name="name" placeholder="Nome do item" required>
                <button type="submit">Adicionar</button>
            </form>
            <form action="/add_bulk/${cartId}" method="post" class="add-form compact">
                <textarea name="items" placeholder="Itens separados por vírgula"></textarea>
                <button type="submit">Adicionar Todos</button>
            </form>
            <div class="actions">
                <button class="btn delete" onclick="finalizeSelection(${cartId})">Finalizar</button>
            </div>
        `;
        manageContainer.appendChild(box);
    }
}

// Mostrar/esconder itens simples (não usado, mas mantido)
function toggleItemList(cartId) {
    const itemsDiv = document.getElementById(`items-${cartId}`);
    itemsDiv.style.display = itemsDiv.style.display === 'none' ? 'block' : 'none';
}

// Finalizar carrinho
function finalizeSelection(cartId) {
    selectedCarts.delete(cartId);
    document.getElementById(`cart-${cartId}`).classList.remove('selected');
    document.getElementById(`dot-${cartId}`).classList.remove('active');
    const box = document.getElementById(`manage-${cartId}`);
    if (box) box.remove();
}

// Popup de aviso elegante
function showPopup(message) {
    document.querySelectorAll('.popup-warning').forEach(el => el.remove());
    
    const popup = document.createElement("div");
    popup.className = "popup-warning";
    popup.innerText = message;
    document.body.appendChild(popup);
    
    setTimeout(() => popup.style.opacity = "1", 10);
    
    setTimeout(() => {
        popup.style.opacity = "0";
        setTimeout(() => popup.remove(), 300);
    }, 3000);
}

// Ações da navbar (não usada atualmente, mas mantida)
function handleNavAction(action) {
    if (selectedCarts.size === 0) {
        showPopup("⚠️ Selecione um carrinho antes de realizar esta ação!");
        return;
    }

    const cartId = Array.from(selectedCarts)[0];

    if (action === "view") {
        window.location.href = "/cart/" + cartId;
    } else if (action === "edit") {
        window.location.href = "/edit/" + cartId;
    } else if (action === "delete") {
        const skipConfirm = localStorage.getItem("skipDeleteConfirm");
        if (skipConfirm === "true") {
            confirmDelete(cartId);
            return;
        }

        const confirmBox = document.createElement("div");
        confirmBox.className = "popup-confirm";
        confirmBox.innerHTML = `
            <p>Tem certeza que deseja deletar este carrinho?</p>
            <label><input type="checkbox" id="skipConfirm"> Não mostrar este aviso novamente</label>
            <div class="actions">
                <button onclick="confirmDelete(${cartId})">Sim</button>
                <button onclick="cancelDelete(this)">Cancelar</button>
            </div>
        `;
        document.body.appendChild(confirmBox);
    }
}

// Confirmar exclusão de carrinho
function confirmDelete(cartId) {
    const skip = document.getElementById("skipConfirm")?.checked;
    if (skip) localStorage.setItem("skipDeleteConfirm", "true");

    fetch(`${API_BASE_URL}/api/carrinhos/${cartId}`, { 
        method: "DELETE",
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`
        }
    })
    .then(response => {
        if (response.ok) {
            showPopup(`🗑️ Carrinho deletado com sucesso!`);
            finalizeSelection(cartId);
            setTimeout(() => location.reload(), 1000);
        } else {
            if (response.status === 401) {
                showPopup('🔒 Sessão expirada. Faça login novamente.');
                setTimeout(() => window.location.href = '/login', 2000);
            } else {
                showPopup("❌ Erro ao deletar carrinho.");
            }
        }
    })
    .catch(() => showPopup("❌ Erro de conexão com o servidor."));

    cancelDelete(document.querySelector(".popup-confirm .actions button:last-child"));
}

// Cancelar exclusão
function cancelDelete(el) {
    el.closest(".popup-confirm").remove();
}

// Abrir pergaminho com itens (SEM DUPLICAÇÃO)
// Abrir pergaminho com itens (CORRIGIDA)
function abrirPergaminho(cartId) {
    const modal = document.getElementById('pergaminho-modal');
    const overlay = document.getElementById('pergaminho-overlay');
    const lista = document.getElementById('lista-itens-modal');
    const som = document.getElementById('som-pergaminho');

    // Limpa a lista e mostra loading
    lista.innerHTML = '<li style="text-align:center; color:#3e2f1c; font-style:italic;">Carregando...</li>';

    fetch(`${API_BASE_URL}/api/carrinhos/${cartId}/itens`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${getAuthToken()}`
        }
    })
    .then(res => {
        if (!res.ok) throw new Error(`Falha na resposta: ${res.status}`);
        return res.json();
    })
    .then(data => {
        lista.innerHTML = '';
        
        if (data.length === 0) {
            lista.innerHTML = '<li style="text-align:center; color:#3e2f1c;">Nenhum item encontrado</li>';
        } else {
            data.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    ${item.name}
                    <button class="btn delete-item-btn" 
                            onclick="deletarItem(${item.id}, this.parentElement)">
                        🗑️
                    </button>
                `;
                lista.appendChild(li);
            });
        }

        overlay.style.display = 'block';
        modal.style.display = 'block';
        som.play();
    })
    .catch(err => {
        console.error('Erro ao carregar itens:', err);
        lista.innerHTML = '<li style="text-align:center; color:#c62828;">Erro ao carregar</li>';
    });
}

// Deletar item específico (COM AUTENTICAÇÃO E URL CORRETA)
function deletarItem(itemId, liElement) {
    if (!confirm('Tem certeza que deseja deletar este item?')) return;

    const token = getAuthToken();
    if (!token) {
        showPopup('🔒 Sessão expirada. Faça login novamente.');
        setTimeout(() => window.location.href = '/login', 2000);
        return;
    }

    fetch(`${API_BASE_URL}/api/itens/${itemId}`, { 
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(res => {
        if (res.ok) {
            liElement.remove();
            showPopup('✅ Item deletado!');
            
            const lista = document.getElementById('lista-itens-modal');
            if (lista && lista.children.length === 0) {
                lista.innerHTML = '<li style="text-align:center; color:#3e2f1c;">Nenhum item encontrado</li>';
            }
        } else {
            if (res.status === 401) {
                showPopup('🔒 Token inválido. Faça login novamente.');
                setTimeout(() => window.location.href = '/login', 2000);
            } else if (res.status === 404) {
                showPopup('❌ Item não encontrado.');
            } else {
                showPopup(`❌ Erro: ${res.status}`);
            }
        }
    })
    .catch(err => {
        console.error('Erro de rede:', err);
        showPopup('🌐 Erro de conexão com o servidor');
    });
}

// Fechar pergaminho
document.addEventListener("DOMContentLoaded", function () {
    const fecharBtn = document.getElementById('fechar-pergaminho');
    const overlay = document.getElementById('pergaminho-overlay');
    
    if (fecharBtn) {
        fecharBtn.addEventListener('click', fecharPergaminho);
    }
    
    if (overlay) {
        overlay.addEventListener('click', fecharPergaminho);
    }
    
    function fecharPergaminho() {
        document.getElementById('pergaminho-modal').style.display = 'none';
        document.getElementById('pergaminho-overlay').style.display = 'none';
    }
});

// Expõe funções globais
window.toggleSelect = toggleSelect;
window.toggleItemList = toggleItemList;
window.finalizeSelection = finalizeSelection;
window.handleNavAction = handleNavAction;
window.abrirPergaminho = abrirPergaminho;