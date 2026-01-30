let galleryImages = [];
let currentIndex = 0;

document.addEventListener("DOMContentLoaded", () => {

  // sirf actual gallery images lo
  document.querySelectorAll(
    '#gallerySlider img[data-gallery="true"]'
  ).forEach(img => {
    galleryImages.push(img.src);
  });

  console.log("Gallery Loaded:", galleryImages);
});

function openGalleryPopup(index) {
  if (!galleryImages.length) return;

  currentIndex = index;
  document.getElementById("popupImage").src =
    galleryImages[currentIndex];

  document.getElementById("galleryPopup")
    .classList.remove("hidden");

  document.body.style.overflow = "hidden";
}

function closeGalleryPopup() {
  document.getElementById("galleryPopup")
    .classList.add("hidden");

  document.body.style.overflow = "";
}

function nextImage() {
  currentIndex = (currentIndex + 1) % galleryImages.length;
  document.getElementById("popupImage").src =
    galleryImages[currentIndex];
}

function prevImage() {
  currentIndex =
    (currentIndex - 1 + galleryImages.length) % galleryImages.length;

  document.getElementById("popupImage").src =
    galleryImages[currentIndex];
}

// ESC key close
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeGalleryPopup();
});
document.addEventListener("input", function (e) {
  if (e.target.classList.contains("phone-input")) {
    e.target.value = e.target.value.replace(/\D/g, "").slice(0, 10);
  }
});
function scrollAmenities(value) {
  document.getElementById('amenitiesScroll').scrollBy({
    left: value,
    behavior: 'smooth'
  });
}
let itiInstances = [];

function initPhoneValidation() {
  itiInstances = [];

  document.querySelectorAll(".phone-input").forEach(input => {

    const iti = window.intlTelInput(input, {
      initialCountry: "auto",
      separateDialCode: true,
      nationalMode: false,
      utilsScript:
        "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/18.2.1/js/utils.js",
      geoIpLookup: cb => {
        fetch("https://ipapi.co/json/")
          .then(res => res.json())
          .then(data => cb(data.country_code))
          .catch(() => cb("IN"));
      }
    });

    itiInstances.push({ input, iti });

    // live validation
    input.addEventListener("input", () => {
      validatePhoneInput(input, iti);
    });
  });
}

function validatePhoneInput(input, iti) {
  const errorEl = input.nextElementSibling;

  if (input.value.trim() === "") {
    errorEl.classList.add("hidden");
    return false;
  }

  if (iti.isValidNumber()) {
    errorEl.classList.add("hidden");
    input.classList.remove("border-red-500");
    return true;
  } else {
    errorEl.classList.remove("hidden");
    input.classList.add("border-red-500");
    return false;
  }
}

/* 🔥 FORM SUBMIT BLOCK */
document.querySelectorAll("form").forEach(form => {
  form.addEventListener("submit", function (e) {

    let valid = true;

    itiInstances.forEach(obj => {
      if (form.contains(obj.input)) {
        if (!validatePhoneInput(obj.input, obj.iti)) {
          valid = false;
        }
      }
    });

    if (!valid) {
      e.preventDefault(); // ❌ stop submit
    }
  });
});

/* init on load */
document.addEventListener("DOMContentLoaded", initPhoneValidation);
function openConfigModal(btn){
  // 1. Button se Data nikaalo
  const bhk = btn.getAttribute('data-bhk');
  
  // Debugging: Console check karein agar value na aaye
  console.log("Saving Configuration:", bhk);

  // 2. UI Update (Modal Text)
  document.getElementById("selectedBHK").innerText = bhk;

  // 3. Backend Input Update (Jo Hidden field hai)
  const hiddenInput = document.getElementById("modalConfigInput");
  if(hiddenInput){
      hiddenInput.value = bhk;
  }

  // 4. Modal Open
  document.getElementById("configModal").classList.remove("hidden");
}

function closeConfigModal(){
  document.getElementById("configModal").classList.add("hidden");
}


  // ✅ Auto Open After 5 seconds
  window.addEventListener("load", () => {
    setTimeout(() => {
      openAutoEnquiryModal();
    }, 5000);
  });

  function openAutoEnquiryModal(title = "Project Details") {
    const modal = document.getElementById("autoEnquiryModal");
    const titleEl = document.getElementById("autoEnquiryTitle");

    if (titleEl) titleEl.innerText = title;

    if (modal) {
      modal.classList.remove("hidden");
      document.body.classList.add("overflow-hidden"); // stop background scroll
    }
  }

  function closeAutoEnquiryModal() {
    const modal = document.getElementById("autoEnquiryModal");
    if (modal) modal.classList.add("hidden");
    document.body.classList.remove("overflow-hidden");
  }

  // ✅ close on outside click
  document.addEventListener("click", function (e) {
    const modal = document.getElementById("autoEnquiryModal");
    if (!modal || modal.classList.contains("hidden")) return;

    if (e.target === modal) closeAutoEnquiryModal();
  });

  function submitAutoEnquiryForm(event) {
    event.preventDefault();

    const name = document.getElementById("enqName").value.trim();
    const phone = document.getElementById("enqPhone").value.trim();
    const email = document.getElementById("enqEmail").value.trim();

    // ✅ example action (you can change)
    console.log("Enquiry Submitted:", { name, phone, email });

    // ✅ Close modal after submit
    closeAutoEnquiryModal();

    // ✅ Redirect / open plan page etc (optional)
    // window.location.href = "/plans/";

    return false;
  }


  function openVirtualVideo() {
  document.getElementById('virtualCover').classList.add('hidden');
  document.getElementById('virtualVideo').classList.remove('hidden');
  document.getElementById('virtualIframe').src =
    "https://www.youtube.com/embed/{{project.youtube_embed_id }}";
}

function closeVirtualVideo() {
  document.getElementById('virtualVideo').classList.add('hidden');
  document.getElementById('virtualCover').classList.remove('hidden');
  document.getElementById('virtualIframe').src = "";
}

  function openVisitModal(){
    document.getElementById("visitModal").classList.remove("hidden");
  }
  function closeVisitModal(){
    document.getElementById("visitModal").classList.add("hidden");
  }

  function openPriceModal(){
    document.getElementById("priceModal").classList.remove("hidden");
  }
  function closePriceModal(){
    document.getElementById("priceModal").classList.add("hidden");
  }

  const modal = document.getElementById('planModal');
  const modalTitle = document.getElementById('modalTitle');

  function openModal(title) {
    modalTitle.innerText = title; 
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
    document.querySelectorAll(".phone-input").forEach(input => {
    const iti = window.intlTelInput(input, {
      initialCountry: "auto",
      separateDialCode: true,
      utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/18.2.1/js/utils.js",
      geoIpLookup: cb => fetch("https://ipapi.co/json").then(r=>r.json()).then(d=>cb(d.country_code)).catch(()=>cb("IN"))
    });
  });
    document.querySelectorAll('.faq-btn').forEach(button => {
    button.addEventListener('click', () => {
      const item = button.closest('.faq-item');
      const content = item.querySelector('.faq-content');
      const icon = item.querySelector('.faq-icon i');

      // Close all other FAQs
      document.querySelectorAll('.faq-item').forEach(other => {
        if (other !== item) {
          other.querySelector('.faq-content').classList.add('hidden');
          other.querySelector('.faq-icon i').classList.remove('fa-minus');
          other.querySelector('.faq-icon i').classList.add('fa-plus');
        }
      });

      // Toggle current FAQ
      content.classList.toggle('hidden');
      icon.classList.toggle('fa-plus');
      icon.classList.toggle('fa-minus');
    });
  });
  window.closeBrochureModal = function () {
  document.getElementById("brochureModal").classList.add("hidden");
};

function scrollAmenities(value){
  document.getElementById('amenitiesScroll').scrollBy({ left:value, behavior:'smooth' });
}
