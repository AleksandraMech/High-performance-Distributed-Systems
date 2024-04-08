const productListItems = document.querySelectorAll('div ul li');

// Iteracja po każdym elemencie <li>
productListItems.forEach(listItem => {
    // Pobranie wartości elementu <h3> wewnątrz bieżącego elementu <li>
    const productName = listItem.querySelector('h3').textContent;
    // Pobranie wartości elementu <p> (ceny) wewnątrz bieżącego elementu <li>
    const productPrice = listItem.querySelector('p').textContent;
    // Wyświetlenie wartości w konsoli
    console.log('Nazwa produktu:', productName);
    console.log('Cena:', productPrice);
});