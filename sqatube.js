// Create and style the main container for the page
document.body.style.fontFamily = 'Arial, sans-serif';
document.body.style.margin = '0';
document.body.style.padding = '0';
document.body.style.boxSizing = 'border-box';

// Create and add the main heading
const heading = document.createElement('h1');
heading.textContent = 'SQATube';
heading.style.textAlign = 'center';
heading.style.backgroundColor = '#ff0000';
heading.style.color = '#ffffff';
heading.style.padding = '20px';
document.body.appendChild(heading);

// Create a container div for the videos
const videoContainer = document.createElement('div');
videoContainer.style.display = 'grid';
videoContainer.style.gridTemplateColumns = 'repeat(3, 1fr)';
videoContainer.style.gap = '20px';
videoContainer.style.padding = '20px';
videoContainer.style.boxSizing = 'border-box';
document.body.appendChild(videoContainer);

// Loop to create 11 video elements
for (let i = 1; i <= 11; i++) {
  const videoDiv = document.createElement('div');
  videoDiv.style.border = '1px solid #ccc';
  videoDiv.style.borderRadius = '5px';
  videoDiv.style.overflow = 'hidden';
  videoDiv.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
  videoDiv.style.textAlign = 'center';

  // Create and add a placeholder image for each video
  const videoThumbnail = document.createElement('img');
  videoThumbnail.src = `https://via.placeholder.com/300x200?text=Video+${i}`;
  videoThumbnail.alt = `Video ${i}`;
  videoThumbnail.style.width = '100%';
  videoThumbnail.style.display = 'block';
  videoDiv.appendChild(videoThumbnail);

  // Create and add a caption below the video
  const videoCaption = document.createElement('p');
  videoCaption.textContent = `Video ${i}`;
  videoCaption.style.margin = '10px 0';
  videoDiv.appendChild(videoCaption);

  // Append the video div to the container
  videoContainer.appendChild(videoDiv);
}
