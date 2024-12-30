document.addEventListener("DOMContentLoaded", function() {
    // Base URL for the icons
    const iconBaseURL = "https://github.com/simple-icons/simple-icons/raw/refs/heads/develop/icons/";

    // Fallback icon if no match is found
    const fallbackIcon = "/assets/default-icon.png";  // Place a default icon in your assets

    // Function to add icon next to the service
    function addIconToService(serviceName, serviceElement) {
        const iconUrl = iconBaseURL + serviceName.toLowerCase().replace(/\s+/g, '-') + ".svg";

        // Try to fetch the icon
        const img = new Image();
        img.onload = function() {
            // Set the icon if the image loads successfully
            const iconElement = document.createElement('img');
            iconElement.src = iconUrl;
            iconElement.alt = serviceName + " Icon";
            iconElement.style.width = "20px";  // Adjust size as necessary
            iconElement.style.marginRight = "8px";  // Space between icon and text
            serviceElement.insertBefore(iconElement, serviceElement.firstChild);
        };

        img.onerror = function() {
            // Fallback to a default icon if the icon is not found
            const iconElement = document.createElement('img');
            iconElement.src = fallbackIcon;
            iconElement.alt = "Default Icon";
            iconElement.style.width = "20px";  // Adjust size as necessary
            iconElement.style.marginRight = "8px";  // Space between icon and text
            serviceElement.insertBefore(iconElement, serviceElement.firstChild);
        };

        img.src = iconUrl;  // Trigger the image load
    }

    // Function to find and add icons to all services
    function addIconsToAllServices() {
        // Find all services by class name
        const services = document.querySelectorAll('.service');

        services.forEach(function(serviceElement) {
            const serviceName = serviceElement.textContent.trim();  // Get the name of the service
            addIconToService(serviceName, serviceElement);  // Add the icon to the service
        });
    }

    // Call the function to add icons to all services
    addIconsToAllServices();
});
