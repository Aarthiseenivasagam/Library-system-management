const bookForm = document.getElementById("bookForm");
const bookName = document.getElementById("bookName");
const author = document.getElementById("author");
const bookList = document.getElementById("bookList");
const search = document.getElementById("search");

let books = [];

function displayBooks(filter = "") {
    bookList.innerHTML = "";

    const filteredBooks = books.filter(book =>
        book.name.toLowerCase().includes(filter.toLowerCase()) ||
        book.author.toLowerCase().includes(filter.toLowerCase())
    );

    if (filteredBooks.length === 0) {
        bookList.innerHTML = "<li>No books found.</li>";
        return;
    }

    filteredBooks.forEach((book, index) => {
        const li = document.createElement("li");
        li.textContent = `${book.name} — ${book.author} `;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";

        deleteButton.onclick = () => {
            books.splice(index, 1);
            displayBooks(search.value);
        };

        li.appendChild(deleteButton);
        bookList.appendChild(li);
    });
}

bookForm.addEventListener("submit", function(event) {
    event.preventDefault();

    books.push({
        name: bookName.value.trim(),
        author: author.value.trim()
    });

    bookName.value = "";
    author.value = "";

    displayBooks(search.value);
});

search.addEventListener("input", function() {
    displayBooks(search.value);
});

displayBooks();