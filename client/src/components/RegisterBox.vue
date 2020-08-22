<template>
    <div id="RegisterBox">
        <div v-if="loading" class="text-center">
            <img src="@/assets/images/misc/dna_spinner_white.svg" alt="loading" class="inline-block" />
        </div>

        <div v-else>
            <div class="relative my-2 rounded">
                <label class="sano-screenreader-only">Email</label>
                <input
                    ref="email_input"
                    v-model.trim="email"
                    class="sano-input rounded appearance-none w-full leading-tight"
                    placeholder="user@email.com"
                    data-cy="email input"
                    type="email"
                    spellcheck="false"
                    @keyup.enter="register"
                    @input="$v.email.$touch"
                />
                <div v-if="$v.email.$dirty">
                    <div v-if="!$v.email.required">Email field is required</div>
                    <div v-if="!$v.email.email">Email field must use an email format</div>
                </div>
                <div class="sano-text-input-focuser"></div>
            </div>

            <div class="text-center relative z-10">
                <div class="text-sano-xs mb-6">
                </div>
                <button
                    style="opacity: 1"
                    class="sano-btn w-full border-white text-white bg-sano-red-orange"
                    data-cy="register button"
                    :disabled="$v.$invalid"
                    @click="register"
                >
                    Register
                </button>
            </div>
        </div>
    </div>
</template>

<script>
const touchMap = new WeakMap();
import { email, required } from 'vuelidate/lib/validators'

export default {
    name: "RegisterBox",
    data() {
        return {
            email: "",
            loading: false,
        };
    },

    validations: {
        email: {
            email,
            required
        }
    },

    methods: {
        register() {
            if(!this.$v.$invalid) {
                this.loading = true;
                this.$api.auth
                    .register(this.email)
                    .then(() => {
                        this.loading = false;
                        this.$router.push({
                            name: "register-thanks",
                            params: { email: this.email },
                        });
                    })
                    .catch(() => {
                        this.loading = false;
                    });
            }
        },
    },
};
</script>

<style scoped lang="scss">
.login-error-holder {
    min-height: 1.3rem;
}
</style>
