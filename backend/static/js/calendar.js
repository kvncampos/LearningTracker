document.addEventListener('DOMContentLoaded', function () {
    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();
    const todayStr = today.toISOString().split('T')[0];

    renderCalendar(currentMonth, currentYear);

    function renderCalendar(month, year) {
        const calendarDates = document.getElementById('calendar-dates');
        const monthYearLabel = document.getElementById('calendar-month-year');
        calendarDates.innerHTML = '';

        const firstDay = new Date(year, month).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        monthYearLabel.textContent = today.toLocaleString('default', { month: 'long' }) + ' ' + year;

        for (let i = 0; i < firstDay; i++) {
            const blank = document.createElement('div');
            blank.className = 'blank';
            calendarDates.appendChild(blank);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dateDiv = document.createElement('div');
            dateDiv.textContent = day;
            dateDiv.className = dateStr === todayStr ? 'today' : '';
            dateDiv.addEventListener('click', function () {
                fetchEntry(dateStr);
            });
            calendarDates.appendChild(dateDiv);
        }
    }

    function fetchEntry(date) {
        fetch(`/get-entry/?date=${date}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('selected-date').textContent = date;
                document.getElementById('description-text').textContent = data.description;
            });
    }
});
