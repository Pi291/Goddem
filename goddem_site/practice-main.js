let score = JSON.parse(localStorage.getItem('score')) || {
         Wins: 0,
         Losses: 0,
         Ties: 0};
      pscore ();
      function Gameplayed (playerMove) {
         const compMove = compchoice();
         let result = '';
         if (playerMove === 'scissors') {
            if (compMove === 'paper') {
            result = 'Win.';
            } else if (compMove === 'rock') {
            result = 'Lose.';
            } else if (compMove === 'scissors') {
            result ='Tie.'; 
            }
         }

         else if (playerMove === 'rock') {
            if (compMove === 'paper') {
            result = 'Lose.';
            } else if (compMove === 'rock') {
            result = 'Tie.';
            } else if (compMove === 'scissors') {
            result ='Win.'; 
            }
         } 
         
         else if (playerMove === 'paper') {
            if (compMove === 'paper') {
            result = 'Tie.';
            } else if (compMove === 'rock') {
            result = 'Win.';
            } else if (compMove === 'scissors') {
            result ='Lose.'; 
            }
         }

         if (result === 'Win.') {
               score.Wins += 1
            }

            else if (result === 'Lose.') {
               score.Losses += 1
            }

            else if (result === 'Tie.') {
               score.Ties += 1
            }
            localStorage.setItem('score', JSON.stringify(score));
            pscore ();
            document.querySelector('.fk-result')
            .innerHTML = result;
            document.querySelector('.fk-moves')
            .innerHTML = `You <img src="Icons/${playerMove}-emoji.png" class="move-icon"> VS <img src="Icons/${compMove}-emoji.png" class="move-icon">Computer.`; 
      }
      function compchoice () {
         let compMove = '';
         const Yourmove = Math.random()
         if (Yourmove >= 0 && Yourmove < 1/3) {
            compMove = 'paper';
         } else if (Yourmove >= 1/3 && Yourmove < 2/3) {
            compMove = 'rock';  
         } else if (Yourmove >= 2/3 && Yourmove <1) {
            compMove = 'scissors'; 
         }
         return compMove;
      }
      function pscore () {
         document.querySelector('.fk-score')
      .innerHTML = `Wins: ${score.Wins}, Losses: ${score.Losses}, Ties: ${score.Ties}`; 
      }