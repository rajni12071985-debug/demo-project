document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const taskInput = document.getElementById('task-input');
    const addBtn = document.getElementById('add-btn');
    const taskList = document.getElementById('task-list');
    const taskCount = document.getElementById('task-count');
    const clearCompletedBtn = document.getElementById('clear-completed');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const dateDisplay = document.getElementById('date-display');

    // App State
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    let currentFilter = 'all';

    // Set Date
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    const today = new Date();
    dateDisplay.textContent = today.toLocaleDateString('en-US', options);

    // Initialization
    renderTasks();

    // Event Listeners
    addBtn.addEventListener('click', addTask);
    
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });

    clearCompletedBtn.addEventListener('click', clearCompleted);

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked
            btn.classList.add('active');
            // Update filter and re-render
            currentFilter = btn.getAttribute('data-filter');
            renderTasks();
        });
    });

    // Functions
    function addTask() {
        const text = taskInput.value.trim();
        if (text === '') return;

        const newTask = {
            id: Date.now().toString(),
            text: text,
            completed: false
        };

        tasks.push(newTask);
        saveTasks();
        taskInput.value = '';
        
        // If we are looking at 'completed' tasks, switch back to 'all' to see the new task
        if (currentFilter === 'completed') {
            document.querySelector('[data-filter="all"]').click();
        } else {
            renderTasks();
        }
    }

    function toggleTaskStatus(id) {
        tasks = tasks.map(task => {
            if (task.id === id) {
                return { ...task, completed: !task.completed };
            }
            return task;
        });
        saveTasks();
        renderTasks();
    }

    function deleteTask(id, element) {
        // Add animation class
        element.classList.add('removing');
        
        // Wait for animation to finish before removing from DOM/State
        setTimeout(() => {
            tasks = tasks.filter(task => task.id !== id);
            saveTasks();
            renderTasks();
        }, 300);
    }

    function clearCompleted() {
        const completedTasks = tasks.filter(task => task.completed);
        if (completedTasks.length === 0) return;

        // Add removing animation to completed elements
        tasks.forEach(task => {
            if (task.completed) {
                const el = document.getElementById(`task-${task.id}`);
                if (el) el.classList.add('removing');
            }
        });

        // Filter and re-render after animation
        setTimeout(() => {
            tasks = tasks.filter(task => !task.completed);
            saveTasks();
            renderTasks();
        }, 300);
    }

    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    function renderTasks() {
        taskList.innerHTML = '';
        let filteredTasks = tasks;

        // Apply filters
        if (currentFilter === 'active') {
            filteredTasks = tasks.filter(task => !task.completed);
        } else if (currentFilter === 'completed') {
            filteredTasks = tasks.filter(task => task.completed);
        }

        updateStats(filteredTasks.length);

        if (filteredTasks.length === 0) {
            let emptyMessage = 'No tasks found. Add one above!';
            let emptyIcon = 'fa-clipboard-list';
            
            if (currentFilter === 'active') {
                emptyMessage = 'No active tasks. You\'re all caught up!';
                emptyIcon = 'fa-check-circle';
            } else if (currentFilter === 'completed') {
                emptyMessage = 'No completed tasks yet.';
                emptyIcon = 'fa-tasks';
            }

            taskList.innerHTML = `
                <div class="empty-state">
                    <i class="fas ${emptyIcon}"></i>
                    <p>${emptyMessage}</p>
                </div>
            `;
            return;
        }

        // Render each task
        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;
            li.id = `task-${task.id}`;

            li.innerHTML = `
                <div class="checkbox-container" aria-label="Toggle completion">
                    <div class="custom-checkbox">
                        <i class="fas fa-check"></i>
                    </div>
                </div>
                <span class="task-text">${escapeHTML(task.text)}</span>
                <button class="delete-btn" aria-label="Delete task">
                    <i class="fas fa-trash-alt"></i>
                </button>
            `;

            // Setup event listeners for the specific elements within this list item
            const checkboxContainer = li.querySelector('.checkbox-container');
            const taskText = li.querySelector('.task-text');
            const deleteBtn = li.querySelector('.delete-btn');

            checkboxContainer.addEventListener('click', () => toggleTaskStatus(task.id));
            taskText.addEventListener('click', () => toggleTaskStatus(task.id));
            deleteBtn.addEventListener('click', () => deleteTask(task.id, li));

            taskList.appendChild(li);
        });
    }

    function updateStats(count) {
        const activeCount = tasks.filter(t => !t.completed).length;
        
        if (currentFilter === 'all') {
            taskCount.textContent = `${activeCount} task${activeCount !== 1 ? 's' : ''} left`;
        } else {
            taskCount.textContent = `${count} task${count !== 1 ? 's' : ''}`;
        }
        
        // Disable clear completed button if no completed tasks exist
        const hasCompleted = tasks.some(t => t.completed);
        clearCompletedBtn.style.opacity = hasCompleted ? '1' : '0.3';
        clearCompletedBtn.style.cursor = hasCompleted ? 'pointer' : 'not-allowed';
        clearCompletedBtn.disabled = !hasCompleted;
    }

    // Utility to prevent XSS
    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});
