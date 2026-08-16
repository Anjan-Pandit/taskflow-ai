const API_URL = "http://127.0.0.1:8000";


// ==========================================
// DOM ELEMENTS
// ==========================================

const taskForm =
    document.getElementById("taskForm");

const taskList =
    document.getElementById("taskList");

const sortTasksSelect =
    document.getElementById("sortTasks");

const filterTasksSelect =
    document.getElementById("filterTasks");

const searchTasksInput =
    document.getElementById("searchTasks");

const titleInput =
    document.getElementById("title");

const descriptionInput =
    document.getElementById("description");

const projectIdInput =
    document.getElementById("projectId");

const priorityInput =
    document.getElementById("priority");

const dueDateInput =
    document.getElementById("dueDate");

const titleError =
    document.getElementById("titleError");

const totalTasks =
    document.getElementById("totalTasks");

const pendingTasks =
    document.getElementById("pendingTasks");

const completedTasks =
    document.getElementById("completedTasks");

const highPriorityTasks =
    document.getElementById("highPriorityTasks");


// ==========================================
// AI QUICK ADD ELEMENTS
// ==========================================

const aiTaskInput =
    document.getElementById("aiTaskInput");

const aiQuickAddButton =
    document.getElementById("aiQuickAddButton");

const aiStatus =
    document.getElementById("aiStatus");


// ==========================================
// LOCAL STORAGE
// ==========================================

function saveTasks(tasks) {

    localStorage.setItem(
        "taskflow_tasks",
        JSON.stringify(tasks)
    );
}


function getCachedTasks() {

    const cachedTasks =
        localStorage.getItem(
            "taskflow_tasks"
        );

    if (!cachedTasks) {
        return [];
    }

    try {

        return JSON.parse(
            cachedTasks
        );

    } catch (error) {

        console.error(
            "Cache error:",
            error
        );

        return [];
    }
}


// ==========================================
// OVERDUE CHECK
// ==========================================

function isOverdue(task) {

    if (task.completed) {
        return false;
    }

    if (!task.due_date) {
        return false;
    }

    const today =
        new Date();

    today.setHours(
        0,
        0,
        0,
        0
    );

    const dueDate =
        new Date(
            task.due_date
        );

    dueDate.setHours(
        0,
        0,
        0,
        0
    );

    return dueDate < today;
}


// ==========================================
// STATISTICS
// ==========================================

function updateStatistics() {

    const tasks =
        getCachedTasks();

    totalTasks.textContent =
        tasks.length;

    pendingTasks.textContent =
        tasks.filter(
            task =>
                !task.completed
        ).length;

    completedTasks.textContent =
        tasks.filter(
            task =>
                task.completed
        ).length;

    highPriorityTasks.textContent =
        tasks.filter(
            task =>
                task.priority === "high"
        ).length;
}


// ==========================================
// SEARCH
// ==========================================

function searchTasks(tasks) {

    const searchText =
        searchTasksInput.value
            .trim()
            .toLowerCase();

    if (!searchText) {
        return tasks;
    }

    return tasks.filter(
        task => {

            const title =
                (
                    task.title ||
                    ""
                ).toLowerCase();

            const description =
                (
                    task.description ||
                    ""
                ).toLowerCase();

            return (
                title.includes(
                    searchText
                ) ||
                description.includes(
                    searchText
                )
            );
        }
    );
}


// ==========================================
// FILTER
// ==========================================

function filterTasks(tasks) {

    const filter =
        filterTasksSelect.value;

    if (filter === "all") {
        return tasks;
    }

    if (filter === "pending") {

        return tasks.filter(
            task =>
                !task.completed
        );
    }

    if (filter === "completed") {

        return tasks.filter(
            task =>
                task.completed
        );
    }

    if (filter === "high") {

        return tasks.filter(
            task =>
                task.priority === "high"
        );
    }

    if (filter === "medium") {

        return tasks.filter(
            task =>
                task.priority === "medium"
        );
    }

    if (filter === "low") {

        return tasks.filter(
            task =>
                task.priority === "low"
        );
    }

    return tasks;
}


// ==========================================
// RENDER TASKS
// ==========================================

function renderTasks(tasks) {

    updateStatistics();

    let visibleTasks =
        searchTasks(tasks);

    visibleTasks =
        filterTasks(
            visibleTasks
        );

    taskList.textContent = "";


    if (
        visibleTasks.length === 0
    ) {

        const message =
            document.createElement(
                "p"
            );

        message.textContent =
            "No tasks found.";

        taskList.appendChild(
            message
        );

        return;
    }


    visibleTasks.forEach(
        task => {

            const taskItem =
                document.createElement(
                    "div"
                );

            taskItem.className =
                "task-item";


            // ==================================
            // PRIORITY CLASS
            // ==================================

            if (
                task.priority === "high"
            ) {

                taskItem.classList.add(
                    "priority-high"
                );
            }

            if (
                task.priority === "medium"
            ) {

                taskItem.classList.add(
                    "priority-medium"
                );
            }

            if (
                task.priority === "low"
            ) {

                taskItem.classList.add(
                    "priority-low"
                );
            }


            // ==================================
            // OVERDUE
            // ==================================

            if (
                isOverdue(task)
            ) {

                taskItem.classList.add(
                    "overdue"
                );
            }


            // ==================================
            // TITLE
            // ==================================

            const title =
                document.createElement(
                    "h3"
                );

            title.textContent =
                task.title;


            // ==================================
            // DESCRIPTION
            // ==================================

            const description =
                document.createElement(
                    "p"
                );

            description.textContent =
                `Description: ${
                    task.description ||
                    "No description"
                }`;


            // ==================================
            // PRIORITY
            // ==================================

            const priority =
                document.createElement(
                    "p"
                );

            priority.textContent =
                `Priority: ${
                    task.priority
                }`;


            // ==================================
            // DUE DATE
            // ==================================

            const dueDate =
                document.createElement(
                    "p"
                );

            dueDate.textContent =
                `Due Date: ${
                    task.due_date ||
                    "Not set"
                }`;


            // ==================================
            // PROJECT
            // ==================================

            const project =
                document.createElement(
                    "p"
                );

            project.textContent =
                `Project ID: ${
                    task.project_id ??
                    "Not assigned"
                }`;


            // ==================================
            // STATUS
            // ==================================

            const status =
                document.createElement(
                    "p"
                );


            if (
                isOverdue(task)
            ) {

                status.textContent =
                    "Status: Overdue";

                status.className =
                    "status-overdue";

            } else if (
                task.completed
            ) {

                status.textContent =
                    "Status: Completed";

                status.className =
                    "status-completed";

            } else {

                status.textContent =
                    "Status: Pending";

                status.className =
                    "status-pending";
            }


            // ==================================
            // ACTIONS
            // ==================================

            const actions =
                document.createElement(
                    "div"
                );

            actions.className =
                "task-actions";


            // ==================================
            // COMPLETE BUTTON
            // ==================================

            const completeButton =
                document.createElement(
                    "button"
                );

            completeButton.textContent =
                task.completed
                    ? "Mark Pending"
                    : "Mark Complete";

            completeButton.addEventListener(
                "click",
                () => {

                    toggleTaskCompletion(
                        task
                    );
                }
            );


            // ==================================
            // EDIT BUTTON
            // ==================================

            const editButton =
                document.createElement(
                    "button"
                );

            editButton.textContent =
                "Edit";

            editButton.addEventListener(
                "click",
                () => {

                    editTask(task);
                }
            );


            // ==================================
            // DELETE BUTTON
            // ==================================

            const deleteButton =
                document.createElement(
                    "button"
                );

            deleteButton.textContent =
                "Delete";

            deleteButton.addEventListener(
                "click",
                () => {

                    deleteTask(
                        task.id
                    );
                }
            );


            // ==================================
            // APPEND ACTIONS
            // ==================================

            actions.appendChild(
                completeButton
            );

            actions.appendChild(
                editButton
            );

            actions.appendChild(
                deleteButton
            );


            // ==================================
            // APPEND TASK CONTENT
            // ==================================

            taskItem.appendChild(
                title
            );

            taskItem.appendChild(
                description
            );

            taskItem.appendChild(
                priority
            );

            taskItem.appendChild(
                dueDate
            );

            taskItem.appendChild(
                project
            );

            taskItem.appendChild(
                status
            );

            taskItem.appendChild(
                actions
            );

            taskList.appendChild(
                taskItem
            );
        }
    );
}


// ==========================================
// LOAD TASKS
// ==========================================

async function loadTasks() {

    try {

        const response =
            await fetch(
                `${API_URL}/tasks/`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load tasks"
            );
        }


        const tasks =
            await response.json();


        saveTasks(tasks);

        renderTasks(tasks);


        console.log(
            "Tasks loaded:",
            tasks
        );


    } catch (error) {

        console.error(
            "Error loading tasks:",
            error
        );


        const cachedTasks =
            getCachedTasks();


        if (
            cachedTasks.length > 0
        ) {

            renderTasks(
                cachedTasks
            );

        } else {

            taskList.textContent = "";

            const message =
                document.createElement(
                    "p"
                );

            message.textContent =
                "Unable to load tasks.";

            taskList.appendChild(
                message
            );
        }
    }
}


// ==========================================
// SORT TASKS
// ==========================================

async function loadSortedTasks(
    sortValue
) {

    try {

        let url =
            `${API_URL}/tasks/`;


        if (
            sortValue === "priority"
        ) {

            url =
                `${API_URL}/tasks/?sort=priority`;
        }


        if (
            sortValue === "dueDate"
        ) {

            url =
                `${API_URL}/tasks/?sort=due_date`;
        }


        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                "Failed to load sorted tasks"
            );
        }


        const tasks =
            await response.json();


        saveTasks(tasks);

        renderTasks(tasks);


    } catch (error) {

        console.error(
            "Sorting error:",
            error
        );

        renderTasks(
            getCachedTasks()
        );
    }
}


// ==========================================
// AI QUICK ADD
// ==========================================

async function analyzeTaskWithAI() {

    const userInput =
        aiTaskInput.value.trim();


    if (!userInput) {

        aiStatus.textContent =
            "Please describe your task first.";

        return;
    }


    aiStatus.textContent =
        "✨ AI is analyzing your task...";

    aiQuickAddButton.disabled =
        true;


    try {

        const response =
            await fetch(
                `${API_URL}/ai/analyze-task`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        title:
                            userInput,

                        description:
                            ""
                    })
                }
            );


        if (!response.ok) {

            let errorData = {};

            try {

                errorData =
                    await response.json();

            } catch (error) {

                console.error(
                    "Could not read error response:",
                    error
                );
            }

            console.error(
                "AI analysis error:",
                errorData
            );

            throw new Error(
                "AI analysis failed"
            );
        }


        const result =
            await response.json();


        console.log(
            "AI Analysis Result:",
            result
        );


        // ==================================
        // FILL TITLE
        // ==================================

        titleInput.value =
            result.title ||
            userInput;


        // ==================================
        // FILL DESCRIPTION
        // ==================================

        descriptionInput.value =
            result.description ||
            "";


        // ==================================
        // FILL PRIORITY
        // ==================================

        const aiPriority =
            String(
                result.priority ||
                "medium"
            )
                .toLowerCase()
                .trim();


        if (
            [
                "low",
                "medium",
                "high"
            ].includes(aiPriority)
        ) {

            priorityInput.value =
                aiPriority;

        } else {

            priorityInput.value =
                "medium";
        }


        // ==================================
        // FILL PROJECT ID
        // ==================================

        if (
            result.project_id !==
                undefined &&
            result.project_id !==
                null &&
            result.project_id !== ""
        ) {

            projectIdInput.value =
                result.project_id;

        } else {

            // PROJECT ID OPTIONAL
            projectIdInput.value =
                "";
        }


        // ==================================
        // FILL DUE DATE
        // ==================================

        let aiDueDate =
            result.due_date ||
            result.dueDate ||
            result.date ||
            "";


        if (aiDueDate) {

            aiDueDate =
                String(
                    aiDueDate
                ).trim();


            if (
                /^\d{4}-\d{2}-\d{2}$/
                    .test(aiDueDate)
            ) {

                dueDateInput.value =
                    aiDueDate;

            } else {

                const parsedDate =
                    new Date(
                        aiDueDate
                    );


                if (
                    !isNaN(
                        parsedDate.getTime()
                    )
                ) {

                    const year =
                        parsedDate.getFullYear();

                    const month =
                        String(
                            parsedDate.getMonth() + 1
                        ).padStart(
                            2,
                            "0"
                        );

                    const day =
                        String(
                            parsedDate.getDate()
                        ).padStart(
                            2,
                            "0"
                        );

                    dueDateInput.value =
                        `${year}-${month}-${day}`;

                } else {

                    dueDateInput.value =
                        "";
                }
            }

        } else {

            dueDateInput.value =
                "";
        }


        // ==================================
        // AI STATUS
        // ==================================

        aiStatus.textContent =
            "✅ AI analyzed the task. Review the details below and click Add Task.";


        console.log(
            "AI filled form:",
            {
                title:
                    titleInput.value,

                description:
                    descriptionInput.value,

                project_id:
                    projectIdInput.value,

                priority:
                    priorityInput.value,

                due_date:
                    dueDateInput.value
            }
        );


        titleInput.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        console.error(
            "AI Quick Add error:",
            error
        );

        aiStatus.textContent =
            "❌ Unable to analyze task. Please try again.";

    } finally {

        aiQuickAddButton.disabled =
            false;
    }
}


// ==========================================
// AI BUTTON
// ==========================================

aiQuickAddButton.addEventListener(
    "click",
    analyzeTaskWithAI
);


// ==========================================
// ADD TASK
// ==========================================

taskForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const title =
            titleInput.value.trim();


        // ==================================
        // TITLE VALIDATION
        // ==================================

        if (!title) {

            titleError.textContent =
                "Title cannot be empty.";

            return;
        }


        titleError.textContent =
            "";


        // ==================================
        // OPTIONAL PROJECT ID
        // ==================================

        const projectIdValue =
            projectIdInput.value.trim();


        let projectId =
            null;


        if (projectIdValue !== "") {

            projectId =
                Number(
                    projectIdValue
                );


            if (
                !Number.isInteger(
                    projectId
                ) ||
                projectId < 1
            ) {

                alert(
                    "Please enter a valid Project ID or leave it empty."
                );

                return;
            }
        }


        // ==================================
        // TASK DATA
        // ==================================

        const taskData = {

            title:
                title,

            description:
                descriptionInput.value.trim(),

            project_id:
                projectId,

            priority:
                priorityInput.value,

            due_date:
                dueDateInput.value ||
                null,

            completed:
                false
        };


        console.log(
            "Creating task:",
            taskData
        );


        try {

            const response =
                await fetch(
                    `${API_URL}/tasks/`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                taskData
                            )
                    }
                );


            if (!response.ok) {

                let errorData = {};

                try {

                    errorData =
                        await response.json();

                } catch (error) {

                    console.error(
                        "Could not read error response:",
                        error
                    );
                }


                console.error(
                    "Create task error:",
                    errorData
                );


                alert(
                    errorData.detail ||
                    "Task could not be created."
                );

                return;
            }


            const newTask =
                await response.json();


            console.log(
                "Task created:",
                newTask
            );


            const currentTasks =
                getCachedTasks();


            currentTasks.push(
                newTask
            );


            saveTasks(
                currentTasks
            );


            renderTasks(
                currentTasks
            );


            // ==================================
            // RESET FORM
            // ==================================

            taskForm.reset();


            priorityInput.value =
                "medium";


            // ==================================
            // RESET AI SECTION
            // ==================================

            aiTaskInput.value =
                "";

            aiStatus.textContent =
                "";


        } catch (error) {

            console.error(
                "Error creating task:",
                error
            );


            alert(
                "Backend connection failed."
            );
        }
    }
);


// ==========================================
// EDIT TASK
// ==========================================

async function editTask(task) {

    const newTitle =
        prompt(
            "Enter new task title:",
            task.title
        );


    if (
        newTitle === null
    ) {
        return;
    }


    const title =
        newTitle.trim();


    if (!title) {

        alert(
            "Title cannot be empty."
        );

        return;
    }


    const newDescription =
        prompt(
            "Enter new description:",
            task.description || ""
        );


    // ==================================
    // OPTIONAL PROJECT ID
    // ==================================

    const updatedTask = {

        title:
            title,

        description:
            newDescription === null
                ? task.description
                : newDescription.trim(),

        completed:
            task.completed,

        project_id:
            task.project_id ??
            null,

        priority:
            task.priority,

        due_date:
            task.due_date
    };


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${task.id}`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            updatedTask
                        )
                }
            );


        if (!response.ok) {

            alert(
                "Task could not be updated."
            );

            return;
        }


        const updatedTaskFromServer =
            await response.json();


        const tasks =
            getCachedTasks();


        const index =
            tasks.findIndex(
                item =>
                    item.id === task.id
            );


        if (index !== -1) {

            tasks[index] =
                updatedTaskFromServer;
        }


        saveTasks(tasks);

        renderTasks(tasks);


    } catch (error) {

        console.error(
            "Error updating task:",
            error
        );


        alert(
            "Backend connection failed."
        );
    }
}


// ==========================================
// COMPLETE / PENDING
// ==========================================

async function toggleTaskCompletion(
    task
) {

    const updatedTask = {

        title:
            task.title,

        description:
            task.description || "",

        completed:
            !task.completed,

        project_id:
            task.project_id ??
            null,

        priority:
            task.priority,

        due_date:
            task.due_date
    };


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${task.id}`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            updatedTask
                        )
                }
            );


        if (!response.ok) {

            alert(
                "Task status could not be updated."
            );

            return;
        }


        const updatedTaskFromServer =
            await response.json();


        const tasks =
            getCachedTasks();


        const index =
            tasks.findIndex(
                item =>
                    item.id === task.id
            );


        if (index !== -1) {

            tasks[index] =
                updatedTaskFromServer;
        }


        saveTasks(tasks);

        renderTasks(tasks);


    } catch (error) {

        console.error(
            "Error updating task status:",
            error
        );


        alert(
            "Backend connection failed."
        );
    }
}


// ==========================================
// DELETE TASK
// ==========================================

async function deleteTask(
    taskId
) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            alert(
                "Task could not be deleted."
            );

            return;
        }


        const tasks =
            getCachedTasks();


        const updatedTasks =
            tasks.filter(
                task =>
                    task.id !== taskId
            );


        saveTasks(
            updatedTasks
        );


        renderTasks(
            updatedTasks
        );


    } catch (error) {

        console.error(
            "Error deleting task:",
            error
        );


        alert(
            "Backend connection failed."
        );
    }
}


// ==========================================
// SEARCH
// ==========================================

searchTasksInput.addEventListener(
    "input",
    () => {

        renderTasks(
            getCachedTasks()
        );
    }
);


// ==========================================
// FILTER
// ==========================================

filterTasksSelect.addEventListener(
    "change",
    () => {

        renderTasks(
            getCachedTasks()
        );
    }
);


// ==========================================
// SORT
// ==========================================

sortTasksSelect.addEventListener(
    "change",
    () => {

        const sortValue =
            sortTasksSelect.value;


        if (
            sortValue === "priority"
        ) {

            loadSortedTasks(
                "priority"
            );

            return;
        }


        if (
            sortValue === "dueDate"
        ) {

            loadSortedTasks(
                "dueDate"
            );

            return;
        }


        loadTasks();
    }
);


// ==========================================
// TITLE VALIDATION
// ==========================================

titleInput.addEventListener(
    "input",
    () => {

        if (
            titleInput.value.trim()
        ) {

            titleError.textContent =
                "";
        }
    }
);


// ==========================================
// PAGE LOAD
// ==========================================

loadTasks();