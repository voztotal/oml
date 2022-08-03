<template>
  <Dialog
    :visible="showModal"
    :style="{ width: '35vw' }"
    :closable="false"
    :modal="true"
  >
    <template #header>
      <h2>{{ $t("views.dial_pattern.new_title") }}</h2>
    </template>
    <div class="card">
      <div class="grid formgrid">
        <div class="field col-12">
          <label id="dial_pattern_prepend">{{
            $t("models.dial_pattern.prepend")
          }}</label>
          <div class="p-inputgroup mt-2">
            <InputText
              id="dial_pattern_prepend"
              :placeholder="$t('forms.dial_pattern.enter_pattern')"
              v-model="dialPattern.prepend"
            />
          </div>
        </div>
        <div class="field col-12">
          <label id="dial_pattern_prefix"
            :class="{
              'p-error':
                repeatedMatchPattern
            }"
          >{{
            $t("models.dial_pattern.prefix")
          }}</label>
          <div class="p-inputgroup mt-2">
            <InputText
              id="dial_pattern_prefix"
              :class="{
                'p-invalid':
                  repeatedMatchPattern
              }"
              @input="inputPatternEvent"
              :placeholder="$t('forms.dial_pattern.enter_pattern')"
              v-model="dialPattern.prefix"
            />
          </div>
          <small v-if="repeatedMatchPattern" class="p-error"
            >Ya existe patron de discado con ese prefijo</small
          >
        </div>
        <div class="field col-12">
          <label
            id="dial_pattern_match_pattern"
            :class="{
              'p-error':
                (v$.dialPattern.match_pattern.$invalid && submitted) ||
                repeatedMatchPattern,
            }"
            >{{ $t("models.dial_pattern.pattern") }}*</label
          >
          <div class="p-inputgroup mt-2">
            <span class="p-inputgroup-addon">
              <i class="pi pi-list"></i>
            </span>
            <InputText
              id="dial_pattern_match_pattern"
              :class="{
                'p-invalid':
                  (v$.dialPattern.match_pattern.$invalid && submitted) ||
                  repeatedMatchPattern,
              }"
              @input="inputPatternEvent"
              :placeholder="$t('forms.dial_pattern.enter_pattern')"
              v-model="v$.dialPattern.match_pattern.$model"
            />
          </div>
          <small
            v-if="
              (v$.dialPattern.match_pattern.$invalid && submitted) ||
              v$.dialPattern.match_pattern.$pending.$response
            "
            class="p-error"
            >{{
              v$.dialPattern.match_pattern.required.$message.replace(
                "Value",
                $t("models.dial_pattern.pattern")
              )
            }}</small
          >
          <small v-if="repeatedMatchPattern" class="p-error"
            >Ya existe patron de discado con esa regla</small
          >
        </div>
      </div>
    </div>
    <template #footer>
      <div class="flex justify-content-end flex-wrap">
        <Button
          class="p-button-danger p-button-outlined mr-2"
          :label="$t('globals.cancel')"
          @click="closeModal"
        />
        <Button :label="$t('globals.save')" @click="save(!v$.$invalid)" />
      </div>
    </template>
  </Dialog>
</template>

<script>
import { useVuelidate } from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { mapActions, mapState } from 'vuex';

export default {
    setup: () => ({ v$: useVuelidate({ $scope: false }) }),
    validations () {
        return {
            dialPattern: {
                match_pattern: { required }
            }
        };
    },
    inject: ['$helpers'],
    props: {
        dialPatterns: {
            type: Array,
            default: () => []
        },
        showModal: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            submitted: false,
            repeatedMatchPattern: false
        };
    },
    computed: {
        ...mapState(['dialPattern'])
    },
    async created () {
        await this.initializeData();
    },
    methods: {
        ...mapActions(['addDialPattern', 'initDialPatternForm']),
        initializeData () {
            this.submitted = false;
            this.repeatedMatchPattern = false;
            this.initDialPatternForm();
        },
        closeModal () {
            this.$emit('handleDialPatternModalEvent', false);
            this.initializeData();
        },
        inputPatternEvent () {
            this.repeatedMatchPattern = this.dialPatterns.find(
                (dp) => (dp.match_pattern === this.dialPattern.match_pattern && dp.prefix === this.dialPattern.prefix)
            );
        },
        async save (isFormValid) {
            this.submitted = true;
            if (!isFormValid || this.repeatedMatchPattern) {
                return null;
            }
            this.addDialPattern(this.dialPattern);
            this.closeModal();
        }
    },
    watch: {
        dialPatterns: {
            handler () {},
            deep: true,
            immediate: true
        }
    }
};
</script>
