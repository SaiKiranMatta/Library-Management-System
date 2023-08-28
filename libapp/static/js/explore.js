document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const subjectList = document.getElementById('subject-list');
    const booksContainer = document.getElementById('books-container');
    const applyFiltersButton = document.getElementById('apply-filters');

    // Function to update subjects based on the selected department
    function updateSubjects() {
        const selectedDepartment = document.querySelector('input[name="dept"]:checked');
        const departmentValue = selectedDepartment ? selectedDepartment.value : '';

        // Make an AJAX request to get the subjects for the selected department
        fetch(`/get_subjects/?dept=${encodeURIComponent(departmentValue)}`)
            .then(response => response.json())
            .then(data => {
                // Clear the subject list
                subjectList.innerHTML = '';

                // Add subjects dynamically based on the AJAX response
                data.subjects.forEach(subject => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `<input type="checkbox" name="subject" value="${subject}" ${data.selected_subjects.includes(subject) ? 'checked' : ''}>${subject}`;
                    subjectList.appendChild(listItem);
                });

                // Enable the "Apply Filters" button after updating subjects
                applyFiltersButton.disabled = false;
            })
            .catch(error => console.error('Error fetching subjects:', error));
    }

    // Function to update books based on selected filters
    function updateBooks() {
        // Get the selected department and subjects
        const selectedDepartment = document.querySelector('input[name="dept"]:checked');
        const departmentValue = selectedDepartment ? selectedDepartment.value : '';
        const selectedSubjects = Array.from(document.querySelectorAll('input[name="subject"]:checked'))
            .map(checkbox => checkbox.value);

        // Make an AJAX request to get the filtered books
        fetch(`/get_books/?dept=${encodeURIComponent(departmentValue)}&subjects=${encodeURIComponent(selectedSubjects.join('&subjects='))}`)
            .then(response => response.json())
            .then(data => {
                // Clear the books container
                const booksContainer = document.getElementById('books-container');
                if (!booksContainer) {
                    console.error('Books container not found.');
                    return;
                }
                booksContainer.innerHTML = '';

                // Add books dynamically based on the AJAX response
                data.books.forEach(book => {
                    const bookTile = document.createElement('div');
                    bookTile.className = 'book-tile';
                    bookTile.innerHTML = `
                        <h3>${book.title}</h3>
                        <p>Author: ${book.author}</p>
                        <p>Quantity: ${book.quantity}</p>
                        <p>Department: ${book.department}</p>
                        <p>Subject: ${book.subject}</p>
                        <img src="${book.image}" alt="${book.title}">
                        <form action="{% url 'book_request' %}" method="post">
                            {% csrf_token %}
                            <input type="hidden" name="book" value="${book.pk}">
                            <button type="submit">Take Book</button>
                        </form>
                    `;
                    booksContainer.appendChild(bookTile);
                });
            })
            .catch(error => console.error('Error fetching books:', error));
    }

    // Event listener for department and subject checkboxes change
    filterForm.addEventListener('change', function() {
        // Enable the "Apply Filters" button when filters are changed
        applyFiltersButton.disabled = false;
    });

    // Event listener for "Apply Filters" button click
    applyFiltersButton.addEventListener('click', function() {
        // Disable the "Apply Filters" button to prevent multiple clicks during update
        applyFiltersButton.disabled = true;
        // Update subjects and books when the button is clicked
        updateSubjects();
        updateBooks();
    });

    // Initial update to display subjects and books based on default selected filters, if any
    updateSubjects();
    updateBooks();
});