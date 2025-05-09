<template>
  <footer class="footer">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <p>© {{ new Date().getFullYear() }} IIA. Crafted with <i class="mdi mdi-heart text-danger"></i> by CharlesShan</p>
            </div>
        </div>
    </div>
</footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.footer-container {
  width: 100%;
  padding: 10px 0;
  margin-top: auto; /* 关键修改：使footer自动填充剩余空间 */
  background-color: transparent;
}
</style>