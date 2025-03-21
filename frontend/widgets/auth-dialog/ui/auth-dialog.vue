<script setup lang="ts">
import { useNotificationsStore } from '~/shared/model/notifications-store'
import { useForm } from '~/shared/model/form'
import { useCurrentAccountStore } from '~/shared/model/current-account-store'
import { useAccessTokenStore } from '~/shared/model/token-store'
import { useAuthDialogOpenedStore } from '../model/opened-store'
import { logIn } from '../api/log-in'
import { signUp } from '../api/sign-up'

const router = useRouter()
const { accessToken } = storeToRefs(useAccessTokenStore())
const { showNotification } = useNotificationsStore()
const { account } = storeToRefs(useCurrentAccountStore())

const { authDialogOpened } = storeToRefs(useAuthDialogOpenedStore())

const { form, setError } = useForm({
    name: '',
    password: '',
})

async function sendLogInRequest() {
    const response = await logIn(form.value.data.name, form.value.data.password)

    if (response.error.value?.data?.error) {
        setError(response.error.value.data.error)
        return
    }

    if (response.data.value?.data) {
        const sessionData = response.data.value.data

        accessToken.value = sessionData.access_token
        account.value = sessionData.account

        showNotification({ message: 'Logged in', type: 'success' })
        authDialogOpened.value = false
        router.push('/dashboard')
    }
}

async function sendSignUpRequest() {
    const response = await signUp(
        form.value.data.name,
        form.value.data.password,
    )

    if (response.error.value?.data?.error) {
        setError(response.error.value.data.error)
        return
    }

    if (response.data.value?.data) {
        const sessionData = response.data.value.data

        accessToken.value = sessionData.access_token
        account.value = sessionData.account

        showNotification({ message: 'Account created', type: 'success' })
        authDialogOpened.value = false
        router.push('/dashboard')
    }
}

function logInWithTestingAccount() {
    form.value.data = {
        name: 'user',
        password: '123456',
    }

    sendLogInRequest()
}
</script>

<template>
    <DialogWindow
        class="p-3.5 w-[44%] min-w-6 sm:p-3"
        data-test-id="authDialog"
        v-model:opened="authDialogOpened"
    >
        <template #triggerButton>
            <button
                class="font-medium text-lg lg:text-base transition-colors hover:text-neutral-300"
            >
                Log in
            </button>
        </template>

        <div class="flex items-start gap-x-6 sm:flex-wrap">
            <img
                src="~/assets/images/abstract-illustration.jpg"
                alt="Abstract wavy illustration"
                class="w-2/5 min-w-2.5 rounded-3xl sm:w-full sm:h-52 sm:object-cover sm:object-top"
            />

            <form
                @submit.prevent=""
                class="p-4 flex-grow flex flex-col gap-y-5"
            >
                <h2 class="text-2xl font-bold">welcome to qna</h2>

                <GoogleLogInButton />

                <TextField
                    v-model="form.data.name"
                    placeholder="name"
                    class="w-full"
                    :error="form.error?.field === 'name'"
                />

                <TextField
                    v-model="form.data.password"
                    field-type="password"
                    placeholder="password"
                    class="w-full"
                    :error="form.error?.field === 'password'"
                />

                <div class="flex gap-5 flex-wrap mt-2 mb-2">
                    <SolidButton
                        @click="sendLogInRequest"
                        data-test-id="logInButton"
                        type="submit"
                    >
                        Log in
                    </SolidButton>

                    <OutlinedButton
                        @click="sendSignUpRequest"
                        data-test-id="signUpButton"
                        type="submit"
                    >
                        Sign up
                    </OutlinedButton>
                </div>

                <div class="text-base">
                    Just want to try the app?
                    <button
                        class="text-amethyst transition-colors hover:text-amethyst-light"
                        @click="logInWithTestingAccount"
                    >
                        Click here
                    </button>
                </div>
            </form>
        </div>
    </DialogWindow>
</template>
