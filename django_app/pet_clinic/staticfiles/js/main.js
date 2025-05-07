// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(function(message) {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
    
    // Form validation for appointment booking
    const appointmentForm = document.querySelector('form[action*="book_appointment"]');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', function(event) {
            const dateInput = document.getElementById('id_date');
            const timeInput = document.getElementById('id_time');
            
            if (dateInput && timeInput) {
                const selectedDate = new Date(dateInput.value + 'T' + timeInput.value);
                const now = new Date();
                
                if (selectedDate < now) {
                    event.preventDefault();
                    alert('Please select a future date and time for your appointment.');
                }
            }
        });
    }
    
    // Dynamic species/breed selection
    const speciesSelect = document.getElementById('id_species');
    const breedInput = document.getElementById('id_breed');
    
    if (speciesSelect && breedInput) {
        speciesSelect.addEventListener('change', function() {
            const species = this.value;
            
            // Clear the breed input when species changes
            breedInput.value = '';
            
            // You could add breed suggestions based on species here
            if (species === 'DOG') {
                breedInput.setAttribute('placeholder', 'E.g., Labrador, Poodle, German Shepherd');
            } else if (species === 'CAT') {
                breedInput.setAttribute('placeholder', 'E.g., Persian, Siamese, Maine Coon');
            } else {
                breedInput.setAttribute('placeholder', '');
            }
        });
    }
    
    // Star rating interaction for reviews
    const reviewForm = document.querySelector('form[action*="review"]');
    if (reviewForm) {
        const ratingSelect = document.getElementById('id_rating');
        const ratingStars = document.createElement('div');
        ratingStars.className = 'rating-stars';
        
        // Create star elements
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.className = 'rating-star';
            star.innerHTML = '☆';
            star.dataset.value = i;
            
            star.addEventListener('click', function() {
                const value = this.dataset.value;
                ratingSelect.value = value;
                
                // Update star display
                document.querySelectorAll('.rating-star').forEach(function(s, index) {
                    if (index < value) {
                        s.innerHTML = '★';
                        s.classList.add('filled');
                    } else {
                        s.innerHTML = '☆';
                        s.classList.remove('filled');
                    }
                });
            });
            
            ratingStars.appendChild(star);
        }
        
        // Insert stars before the select element
        ratingSelect.parentNode.insertBefore(ratingStars, ratingSelect);
        ratingSelect.style.display = 'none';
        
        // Set initial stars based on selected value
        if (ratingSelect.value) {
            const value = parseInt(ratingSelect.value);
            document.querySelectorAll('.rating-star').forEach(function(s, index) {
                if (index < value) {
                    s.innerHTML = '★';
                    s.classList.add('filled');
                }
            });
        }
    }
    
    // Search form validation
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            const searchInput = this.querySelector('input[name="search_query"]');
            if (searchInput && searchInput.value.trim() === '') {
                event.preventDefault();
                // Clear any previous search results by redirecting to the home page
                window.location.href = window.location.pathname;
            }
        });
    }
});