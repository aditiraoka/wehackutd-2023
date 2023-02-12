let index = 0;
let correct = 0;
let incorrect = 0;
let opts = [];
let total = quizData.length;
let questionBox = document.getElementById("questionBox");
let allInputs = document.querySelectorAll("input[type='radio']");

const loadQuestion = () => {
  if (total === index) {
    return quizEnd();
  }
  reset();
  const data = quizData[index];
  questionBox.innerHTML = `${index + 1}) ${data.question}`;
  allInputs[0].nextElementSibling.innerText = data.a;
  allInputs[1].nextElementSibling.innerText = data.b;
};

document.querySelector("#submit").addEventListener(
  "click",
  function () {
    var checked_gender = document.querySelector(
      'input[name = "option"]:checked',
    );
    if (checked_gender != null) {
      const data = quizData[index];
      const ans = getAnswer();
      opts.push(ans)
      if (ans === data.correct) {
        correct++;
      } else {
        incorrect++;
      }
      index++;
      loadQuestion();
    } else {
      alert("Please Select One Option.");
    }
  },
);

const getAnswer = () => {
  let ans;
  allInputs.forEach((inputEl) => {
    if (inputEl.checked) {
      ans = inputEl.value;
    }
  });
  return ans;
};

const reset = () => {
  allInputs.forEach((inputEl) => {
    inputEl.checked = false;
  });
};

const quizEnd = () => {

  document.getElementsByClassName("container")[0].innerHTML = `
       <div class="col">
            <h3 class="w-100" style="text-align:center;"> 
            YOU HAVE SCORED ${correct} OUT OF ${total}</h3>
            <div class="im" style="text-align:center;">
                <img src="../images/lowscore.jpg" alt="image" height="300">
            </div>
            <h4 class="w-100" style="text-align:center;"> 
            <form action="http://127.0.0.1:5000/register" method="POST">
            <a href="../index.html" style="text-decoration:none;">RETURN TO HOMEPAGE</a></h4>
            </form>           
       </div>
   `;

  if (correct >= 0 && correct <= 1) {
    document.getElementsByClassName("container")[0].innerHTML = `
       <div class="col">
            <h3 class="w-100" style="text-align:center;"> 
            YOU HAVE SCORED ${correct} OUT OF ${total}</h3>
            <div class="im" style="text-align:center;">
                <img src="../images/lowscore.jpg" alt="image" height="300">
            </div>
            <h4 class="w-100" style="text-align:center;"> 
            <a href="../index.html" style="text-decoration:none;">RETURN TO HOMEPAGE</a></h4>
           
       </div>
   `;
  } else if (correct >= 2 && correct <= 4) {
    document.getElementsByClassName("container")[0].innerHTML = `
        <div class="col">
        <h3 class="w-100" style="text-align:center;"> 
            YOU HAVE SCORED ${correct} OUT OF ${total}</h3>
            <div class="im" style="text-align:center;">
                <img src="../images/midscore.jpg" alt="image" height="300">
            </div>
            <h4 class="w-100" style="text-align:center;"> 
            <a href="../index.html" style="text-decoration:none;">RETURN TO HOMEPAGE</a></h4>
           
        </div>
    `;
  } else {
    document.getElementsByClassName("container")[0].innerHTML = `
        <div class="col">
        <h3 class="w-100" style="text-align:center;"> 
            YOU HAVE SCORED ${correct} OUT OF ${total}</h3>
            <div class="im" style="text-align:center;">
                <img src="../images/highscore.jpg" alt="image" height="300">
            </div>
            <h4 class="w-100" style="text-align:center;"> 
            <a href="../index.html" style="text-decoration:none;">RETURN TO HOMEPAGE</a></h4>
           
        </div>
    `;
  }
};

loadQuestion(index);
