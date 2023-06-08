var sentences = [];
var audioURLs = [];
var currentSentenceIndex = 0;

function loadSentences() {
    // Load CSV file and parse the sentences
    fetch("../student_recordings.csv")
        .then(response => response.text())
        .then(csvData => {
            // Split CSV data by newline
            var rows = csvData.split('\n');
            // Iterate over each row
            for (var i = 1; i < rows.length; i++) {
                // Split row by comma and assign second attribute to sentence
                var sentence = rows[i].split(',')[1];
                var audioLink = rows[i].split(',')[0];
                // Add sentence and audio to the arrays
                sentences.push(sentence);
                audioURLs.push(audioLink);
            }
            // Display the first sentence
            displaySentence(currentSentenceIndex);
        })
        .catch(error => {
        console.error('Error:', error);
    });
}

function displaySentence(index) {
    var sentenceContainer = document.getElementById('sentenceContainer');
    var audioContainer = document.getElementById('audioContainer');
    var selectedWordContainer = document.getElementById('selectedWordContainer');

    // Clear previous sentence and audio
    sentenceContainer.innerHTML = '';
    selectedWordContainer.innerHTML = '';
    audioContainer.innerHTML = '';

    // Split sentence into words
    var words = sentences[index].split(' ');

    // Create a new span element for each word
    words.forEach(function(word) {
        var wordSpan = document.createElement('span');
        wordSpan.className = 'word';
        wordSpan.innerText = word + ' ';
        wordSpan.addEventListener('click', function() {
            displaySelectedWord(word);
        });
        sentenceContainer.appendChild(wordSpan);

    });

    var audioButton = document.createElement('button');
    audioButton.innerText = 'Play Audio';
    audioButton.addEventListener('click', function() {
        playAudio(index);
    });
    audioContainer.appendChild(audioButton);
}

function displaySelectedWord(word) {
    var selectedWordContainer = document.getElementById('selectedWordContainer');
    selectedWordContainer.innerText = word;
}

function playAudio(index) {
    var audioURL = audioURLs[index];
    var audio = new Audio(audioURL);
    audio.play();
}

function loadNextSentence() {
    // Increment the current sentence index
    currentSentenceIndex++;

    // Check if the index exceeds the sentence count
    if (currentSentenceIndex >= sentences.length) {
        // Display a message when all sentences have been shown
        alert('No more sentences!');
    } else {
        // Display the next sentence
        displaySentence(currentSentenceIndex);
    }
}

// Load sentences when the page is loaded
document.addEventListener('DOMContentLoaded', loadSentences);
