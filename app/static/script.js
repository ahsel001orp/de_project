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

    async  function post_request(){
        const guest_tg = document.getElementById("tg").value;
        if (guest_tg.startsWith("@")){
        const guest={
          "name" : document.getElementById("name").value,
          "tg" : guest_tg,
          "message" : document.getElementById("message").value
        };
        try {
        const response = await fetch('/send_message',{
          method: "POST",
          headers: {
          "Content-Type": "application/json"
        }, 
        body: JSON.stringify(guest)
        });
        const result = await response.json();
        if (result["ID"] != "OK"){alert("Что то пошло не так 😢");}
        else {alert("Сообщение отправлено!!!спасибо за интерес");}
      } catch (error) {
      console.error("Error:", error);
      }
    }
    else {alert("Ваш телеграм в формате @ahsel001orp");}
      }