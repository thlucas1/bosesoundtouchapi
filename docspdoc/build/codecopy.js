// add event listener to call function after window has been completely loaded.
window.addEventListener("load", codecopyAddLinkButtons, false);

// ********************************************************************
// add "Copy to Clipboard" button to all code hi-lite blocks.
// ********************************************************************
function codecopyAddLinkButtons(){

    // get list of all code hilite blocks.
    const codehilites = document.querySelectorAll("div.codehilite")

    // add "copy" button to each element.
    codehilites.forEach(div => {
        const btnCopy = document.createElement("button")
        btnCopy.innerHTML = "Copy to Clipboard"
        btnCopy.addEventListener("click", codecopyClick)
	btnCopy.style.top = "0px"
	btnCopy.style.right = "0px"
        div.append(btnCopy)
    })
}


// ********************************************************************
// handles the button click event.
// copies the code hi-lite text to the clipboard.
// ********************************************************************
function codecopyClick(evt) {

    // get the children of the parent element.
    const { children } = evt.target.parentElement

    // grab the second element (we append the copy button on afterwards, so the first will be the code element).
    // destructure the innerText from the code block.
    const { innerText } = Array.from(children)[0]

    // copy all of the code to the clipboard.
    copyToClipboard(innerText)

    // inform the user it worked.
    evt.target.innerHTML = "Code Copied to Clipboard"

    // set button text back to normal after 2 seconds.
    setTimeout(function() { evt.target.innerHTML = "Copy to Clipboard"; }, 2000);
}


// ********************************************************************
// copies data to the clipboard.
// ********************************************************************
const copyToClipboard = str => {
  const el = document.createElement("textarea") // Create a <textarea> element
  el.value = str // Set its value to the string that you want copied
  el.setAttribute("readonly", "") // Make it readonly to be tamper-proof
  el.style.position = "absolute"
  el.style.left = "-9999px" // Move outside the screen to make it invisible
  document.body.appendChild(el) // Append the <textarea> element to the HTML document
  const selected =
    document.getSelection().rangeCount > 0 // Check if there is any content selected previously
      ? document.getSelection().getRangeAt(0) // Store selection if found
      : false // Mark as false to know no selection existed before
  el.select() // Select the <textarea> content
  document.execCommand("copy") // Copy - only works as a result of a user action (e.g. click events)
  document.body.removeChild(el) // Remove the <textarea> element
  if (selected) {
    // If a selection existed before copying
    document.getSelection().removeAllRanges() // Unselect everything on the HTML document
    document.getSelection().addRange(selected) // Restore the original selection
  }
}
