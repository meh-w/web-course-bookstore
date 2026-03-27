document.addEventListener("DOMContentLoaded", function() {
    
    const emailInput = document.getElementById("id_email");
    const passwordInput = document.getElementById("id_password1");
    const confirmPasswordInput = document.getElementById("id_password2");
    const registerForm = document.getElementById("registration-form");
    
    if (!emailInput || !passwordInput || !confirmPasswordInput || !registerForm) {
        console.error("Не найдены поля формы!");
        return;
    }
    
    const emailError = document.createElement("div");
    emailError.className = "validation-message";
    emailInput.parentNode.appendChild(emailError);
    
    const passwordError = document.createElement("div");
    passwordError.className = "validation-message";
    passwordInput.parentNode.appendChild(passwordError);
    
    const confirmError = document.createElement("div");
    confirmError.className = "validation-message";
    confirmPasswordInput.parentNode.appendChild(confirmError);
    
    let emailFormatValid = false;
    
    function showMessage(element, message, isError = true) {
        if (!element) return;
        element.textContent = message;
        element.style.color = isError ? "#dc3545" : "#198754";
        element.style.fontSize = "0.875rem";
        element.style.marginTop = "0.25rem";
    }
    
    function validateEmailFormat(email) {
        if (!email) return false;
        
        if (email.length > 254) {
            return false;
        }
        
        const basicRegex = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;
        if (!basicRegex.test(email)) {
            return false;
        }
        
        const atIndex = email.indexOf('@');
        const localPart = email.substring(0, atIndex);
        const domain = email.substring(atIndex + 1);
        
        if (localPart.length === 0) return false;
        
        if (localPart.length > 64) return false;
        
        if (localPart.startsWith('.') || localPart.endsWith('.')) return false;
        
        if (localPart.includes('..')) return false;
        
        const allowedLocalChars = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+$/;
        if (!allowedLocalChars.test(localPart)) return false;
        
        
        if (domain.length === 0) return false;
        
        if (domain.startsWith('.') || domain.endsWith('.')) return false;
        
        if (domain.includes('..')) return false;
        
        if (!domain.includes('.')) return false;
        
        const allowedDomainChars = /^[a-zA-Z0-9.-]+$/;
        if (!allowedDomainChars.test(domain)) return false;
        
        const domainParts = domain.split('.');
        for (const part of domainParts) {
            if (part.length === 0) return false;
            if (part.startsWith('-') || part.endsWith('-')) return false;
            if (!/[a-zA-Z]/.test(part)) return false;
        }
        
        const lastPart = domainParts[domainParts.length - 1];
        if (lastPart.length < 2) return false;
        
        return true;
    }
    
    function checkEmailFormat(email) {
        if (!email) {
            showMessage(emailError, "");
            emailFormatValid = false;
            return false;
        }
        
        if (!validateEmailFormat(email)) {
            showMessage(emailError, "Некорректный формат email.");
            emailFormatValid = false;
            return false;
        }
        
        showMessage(emailError, "Формат email верный", false);
        emailFormatValid = true;
        return true;
    }
    
    async function checkEmailDnsAndUnique(email) {
        if (!email || !emailFormatValid) {
            return false;
        }
        
        showMessage(emailError, "Проверка домена и уникальности...", false);
        
        try {
            const response = await fetch(`/users/check-email/?email=${encodeURIComponent(email)}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Ответ сервера:", data);
            
            if (data.valid) {
                showMessage(emailError, "Email доступен", false);
                emailDnsUniqueValid = true;
                return true;
            } else {
                let errorMessage = data.message;
                if (errorMessage.includes("no valid MX records") || errorMessage.includes("deliverability")) {
                    errorMessage = "Домен не существует или не принимает почту";
                } else if (errorMessage.includes("domain name")) {
                    errorMessage = "Некорректный домен";
                }
                showMessage(emailError, `${errorMessage}`);
                emailDnsUniqueValid = false;
                return false;
            }
        } catch (error) {
            console.error("Ошибка AJAX:", error);
            showMessage(emailError, "Ошибка проверки домена");
            emailDnsUniqueValid = false;
            return false;
        }
    }
    
    function checkPassword(password) {
        if (!password) {
            showMessage(passwordError, "");
            return false;
        }
        
        if (password.length < 6) {
            showMessage(passwordError, "Пароль должен быть не менее 6 символов");
            return false;
        } else {
            showMessage(passwordError, "Пароль подходит", false);
            return true;
        }
    }
    
    function checkPasswordMatch(password, confirm) {
        if (!confirm) {
            showMessage(confirmError, "");
            return false;
        }
        
        if (password !== confirm) {
            showMessage(confirmError, "Пароли не совпадают");
            return false;
        } else {
            showMessage(confirmError, "Пароли совпадают", false);
            return true;
        }
    }
    
    emailInput.addEventListener("input", function() {
        const email = this.value.trim();
        checkEmailFormat(email);
        if (!emailFormatValid) {
            emailDnsUniqueValid = false;
        }
    });
    
    emailInput.addEventListener("blur", async function() {
        const email = this.value.trim();
        
        if (!email) {
            showMessage(emailError, "Введите email");
            emailFormatValid = false;
            emailDnsUniqueValid = false;
            return;
        }
        
        const formatValid = checkEmailFormat(email);
        
        if (formatValid) {
            await checkEmailDnsAndUnique(email);
        } else {
            emailDnsUniqueValid = false;
        }
    });
    
    passwordInput.addEventListener("input", function() {
        checkPassword(this.value);
        checkPasswordMatch(this.value, confirmPasswordInput.value);
    });
    
    passwordInput.addEventListener("blur", function() {
        checkPassword(this.value);
        checkPasswordMatch(this.value, confirmPasswordInput.value);
    });
    
    confirmPasswordInput.addEventListener("input", function() {
        checkPasswordMatch(passwordInput.value, this.value);
    });
    
    confirmPasswordInput.addEventListener("blur", function() {
        checkPasswordMatch(passwordInput.value, this.value);
    });
    
    registerForm.addEventListener("submit", async function(e) {
        let hasError = false;
        
        const email = emailInput.value.trim();
        
        if (!email) {
            showMessage(emailError, "Введите email");
            hasError = true;
        } else {
            const formatValid = checkEmailFormat(email);
            if (!formatValid) {
                hasError = true;
            } else {
                const dnsValid = await checkEmailDnsAndUnique(email);
                if (!dnsValid) {
                    hasError = true;
                }
            }
        }
        
        const password = passwordInput.value;
        if (!checkPassword(password)) {
            hasError = true;
        }
        
        const confirm = confirmPasswordInput.value;
        if (!checkPasswordMatch(password, confirm)) {
            hasError = true;
        }
        
        if (hasError) {
            e.preventDefault();
        }
    });
    
    console.log("JS валидация загружена");
});
