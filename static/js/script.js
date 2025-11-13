// Conjunto de carrinhos selecionados
let selectedCarts = new Set();

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

// Mostrar/esconder itens simples (não o pergaminho)
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

// Popup de aviso
function showPopup(message) {
    const popup = document.createElement("div");
    popup.className = "popup-warning";
    popup.innerText = message;
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 3000);
}

// Ações da navbar
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

// Confirmar exclusão
function confirmDelete(cartId) {
    const skip = document.getElementById("skipConfirm")?.checked;
    if (skip) localStorage.setItem("skipDeleteConfirm", "true");

    fetch(`/delete/${cartId}`, { method: "POST" })
        .then(response => {
            if (response.ok) {
                showPopup(`🗑️ Carrinho ${cartId} deletado com sucesso!`);
                finalizeSelection(cartId);
            } else {
                showPopup("❌ Erro ao deletar carrinho.");
            }
        })
        .catch(() => showPopup("❌ Erro de conexão com o servidor."));

    cancelDelete(document.querySelector(".popup-confirm .actions button:last-child"));
}

// Cancelar exclusão
function cancelDelete(el) {
    el.closest(".popup-confirm").remove();
}

// Abrir pergaminho com itens
function abrirPergaminho(cartId) {
    const modal = document.getElementById('pergaminho-modal');
    const overlay = document.getElementById('pergaminho-overlay');
    const lista = document.getElementById('lista-itens-modal');
    const som = document.getElementById('som-pergaminho');

    lista.innerHTML = '';

    fetch(`/api/carrinhos/${cartId}/itens`)
        .then(res => res.json())
        .then(data => {
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.name;

                const btn = document.createElement('button');
                btn.textContent = '🗑️';
                btn.className = 'delete-item-btn';
                btn.onclick = () => deletarItem(item.id, li);

                li.appendChild(btn);
                lista.appendChild(li);
            });

            overlay.style.display = 'block';
            modal.style.display = 'block';
            som.play();
        });
}

// Deletar item específico
function deletarItem(itemId, liElement) {
    fetch(`/api/itens/${itemId}`, { method: 'DELETE' })
        .then(res => {
            if (res.ok) {
                liElement.remove();
            } else {
                alert("Erro ao deletar item.");
            }
        });
}

// Fechar pergaminho
document.addEventListener("DOMContentLoaded", function () {
    const fecharBtn = document.getElementById('fechar-pergaminho');
    if (fecharBtn) {
        fecharBtn.addEventListener('click', () => {
            document.getElementById('pergaminho-modal').style.display = 'none';
            document.getElementById('pergaminho-overlay').style.display = 'none';
        });
    }
});

// expõe funções globais
window.toggleSelect = toggleSelect;
window.toggleItemList = toggleItemList;
window.finalizeSelection = finalizeSelection;
window.handleNavAction = handleNavAction;
window.abrirPergaminho = abrirPergaminho;