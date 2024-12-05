const socket = io();

socket.on("connect", () => console.log("Connected to the server."));
socket.on("disconnect", () => console.log("Disconnected from the server."));

const generateButton = document.getElementById("generate-button");
const outputImageContainer = document.getElementById("output-image-container");

generateButton.addEventListener("click", () => {
    const prompt = document.getElementById("prompt-textarea").value;
    if (!prompt) {
        alert("Please enter a prompt.");
        return;
    }

    // Combine all the data
    const generationData = {
        prompt: document.getElementById("prompt-textarea").value,
        negative_prompt: document.getElementById("negative-prompt-textarea").value,
        num_inference_steps: parseInt(document.getElementById("iterations-input").getAttribute('value')),
        guidance_scale: parseFloat(document.getElementById("guidance-input").getAttribute('value')),
        width: parseInt(document.getElementById("width-input").getAttribute('value')),
        height: parseInt(document.getElementById("height-input").getAttribute('value')),
        seed: parseInt(document.getElementById("seed-input").value) || null,
        scheduler: document.getElementById("scheduler-input").getAttribute('value')
    };

    console.log(generationData)

    // Send data to the server
    socket.emit("start_generation", generationData);
});


socket.on("generation_completed", (data) => {
    let outputImage = document.getElementById("output-image");
    if (!outputImage) {
        outputImage = document.createElement("img");
        outputImage.id = "output-image";
        outputImageContainer.appendChild(outputImage);
    }
    outputImage.src = `/outputs/${data.filename}`;
    outputImage.alt = "Generated Image";
});

socket.on("update_queue", (data) => {
    // updateQueueUI(data.queue);
});

// function updateQueueUI(queue) {
//     // Update Queue Elements Here

//     document.querySelectorAll(".cancel-queue-item").forEach((button) => {
//         button.addEventListener("click", (event) => {
//             const queueItem = event.target.closest(".queue-item");
//             const index = queueItem.getAttribute("data-index");
//             socket.emit("cancel_queue_item", { index: parseInt(index, 10) });
//         });
//     });
// }

