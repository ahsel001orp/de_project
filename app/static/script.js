var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");

    document.querySelectorAll('.image-link').forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            modal.style.display = "block";
            modalImg.src = this.href;
        });
    });

    var span = document.getElementsByClassName("close")[0];

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

// document.addEventListener('DOMContentLoaded', () => {
//     const navLinks = document.querySelectorAll('.nav-links a');
//     const pages = document.querySelectorAll('.page');

//     navLinks.forEach(link => {
//         link.addEventListener('click', (e) => {
//             e.preventDefault();
//             const targetId = link.getAttribute('href').substring(1);
            
//             pages.forEach(page => {
//                 page.classList.remove('active');
//             });

//             const targetPage = document.getElementById(targetId);
//             targetPage.classList.add('active');
            
//             // Optional: Scroll to top of the page
//             window.scrollTo(0, 0);
//         });
//     });

//     // Optional: Add form submission handling
//     const contactForm = document.querySelector('.contact-form');
//     contactForm.addEventListener('submit', (e) => {
//         e.preventDefault();
//         alert('Сообщение отправлено! Спасибо за ваш интерес.');
//         contactForm.reset();
//     });
// });