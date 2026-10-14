const coin = (x = 74.6, y = 121.8) => `<circle cx="${x}" cy="${y}" r="10.6" fill="#fdd83e" stroke="#4b1a0d" stroke-width="3.4"/>`
 + `<circle cx="${x}" cy="${y}" r="7.6" fill="none" stroke="#eba516" stroke-width="1.5"/>`
 + `<path d="M${x - 5.6} ${y - 1.4}L${x + 1.8} ${y - 8.4}M${x - 3.6} ${y + 4.4}L${x + 6} ${y - 5}" stroke="#ffe680" stroke-width="1.4" stroke-linecap="round"/>`
 + `<path d="M${x - 2.4} ${y - 8.2}q2.2-1.2 4.6-.4" fill="none" stroke="#fff8d6" stroke-width="1.5" stroke-linecap="round"/>`;
module.exports = { coin };
