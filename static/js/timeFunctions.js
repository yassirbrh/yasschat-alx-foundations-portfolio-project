export function calculateTimeDifference(targetTimestamp) {
    const months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];

    // Parse the target timestamp string into a Date object
    const targetDate = new Date(targetTimestamp);

    // Get the current time
    const currentDate = new Date();

    // Calculate the time difference in milliseconds
    const timeDifference = currentDate.getTime() - targetDate.getTime();

    // Calculate days, hours, minutes, and seconds
    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor(timeDifference / (1000 * 60 * 60)) % 24;
    const minutes = Math.floor(timeDifference / (1000 * 60)) % 60;
    const seconds = Math.floor(timeDifference / 1000) % 60;

    // Get the day and month of the target date
    const targetDay = targetDate.getDate();
    const targetMonth = months[targetDate.getMonth()];

    // Return an object with the calculated values
    return {
        days,
        hours,
        minutes,
        seconds,
        targetDay,
        targetMonth
    };
}

export function isSameDay(date1, date2) {
    return date1.getDate() === date2.getDate() && date1.getMonth() === date2.getMonth() && date1.getFullYear() === date2.getFullYear();
}

export function isYesterday(date1, date2) {
    const yesterday = new Date(date2);
    yesterday.setDate(date2.getDate() - 1);
    return isSameDay(date1, yesterday);
}

export function formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

export function formatDate(date) {
    const options = { month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}
