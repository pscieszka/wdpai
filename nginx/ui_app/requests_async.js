function addUserToList(user) {
    const userList = document.getElementById("userList");

    const userDiv = document.createElement('div');
    userDiv.className = 'user';
    userDiv.setAttribute('user-id', user.id); 

    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';

    const nameDiv = document.createElement('div');
    nameDiv.className = 'name';
    nameDiv.textContent = `${user.first_name} ${user.last_name}`;
    contentDiv.appendChild(nameDiv);

    const roleDiv = document.createElement('div');
    roleDiv.className = 'role';
    roleDiv.textContent = user.role;
    contentDiv.appendChild(roleDiv);

    const buttonDiv = document.createElement('div');
    buttonDiv.className = 'button';

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-button';

    const deleteImg = document.createElement('img');
    deleteImg.src = 'Button.png'; 
    deleteImg.style.width = '40px';
    deleteImg.style.height = '40px';

    deleteBtn.appendChild(deleteImg);
    buttonDiv.appendChild(deleteBtn);

    userDiv.appendChild(contentDiv);
    userDiv.appendChild(buttonDiv);

    userList.appendChild(userDiv);

    deleteBtn.addEventListener('click', async function() {
        const userId = user.id;
        try {
            await fetch(`http://localhost:8000/${userId}`, {
                method: 'DELETE',
            });
            userList.removeChild(userDiv); 
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    });
}


document.getElementById('userForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const firstName = document.getElementById("first-name").value;
    const lastName = document.getElementById("last-name").value;
    const role = document.getElementById("role").value;

    const newUser = {
        first_name: firstName,
        last_name: lastName,
        role: role
    };

    try {
        const response = await fetch('http://localhost:8000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newUser)
        });

        const createdUser = await response.json();
        addUserToList(createdUser); 

        document.getElementById("userForm").reset();
    } catch (error) {
        console.error('Error adding user:', error);
    }
});

async function fetchAndDisplayUsers() {
    try {
        const response = await fetch('http://localhost:8000/');  
        const users = await response.json();

        users.forEach(user => {
            addUserToList(user);
        });
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

window.addEventListener('load', fetchAndDisplayUsers);

