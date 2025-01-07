<script lang="ts">
    import { Camera, X } from "lucide-svelte";

    let { handleSearch, handleImageUpload } = $props();
    import { searchState } from "../routes/shared.svelte";

    let searchInput = $state("");
    let fileInput: HTMLInputElement = $state();

    function handleSubmit() {
        handleSearch(searchInput);
    }

    function handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            searchState.previewUrl = URL.createObjectURL(file);
            handleImageUpload(file);
        }
        event.target.value = "";
    }

    function handleTypeChange(e: Event) {
        const select = e.target as HTMLSelectElement;
        searchState.type = select.value;
        searchInput = "";
    }

    function clearPreview() {
        searchState.previewUrl = "";
        if (searchState.previewUrl) {
            URL.revokeObjectURL(searchState.previewUrl);
        }
    }
</script>

<div class="search-container">
    <div class="search-box">
        <div class="search-input-group">
            <select
                class="type-select"
                value={searchState.type}
                onchange={handleTypeChange}
            >
                <option value="recipe">找食譜</option>
                <option value="ingredient">找食材</option>
            </select>

            <input
                type="text"
                bind:value={searchInput}
                placeholder={searchState.type === "recipe"
                    ? "輸入食譜名稱..."
                    : "輸入食材名稱..."}
                onkeyup={(e) => e.key === "Enter" && handleSubmit()}
            />
            <button class="search-btn" onclick={handleSubmit}>
                <!-- <Search size={20}/> -->
                搜尋
            </button>
        </div>

        <div class="divider">或</div>

        <div class="image-upload">
            <input
                type="file"
                bind:this={fileInput}
                accept="image/*"
                onchange={handleFileChange}
                style="display: none"
            />
            <button class="upload-btn" onclick={() => fileInput.click()}>
                <Camera size={20} />
                <span
                    >上傳圖片{searchState.type === "recipe"
                        ? "搜尋食譜"
                        : "搜尋食材"}</span
                >
            </button>
            {#if searchState.previewUrl}
                <div class="preview-container">
                    <img src={searchState.previewUrl} alt="Preview" class="preview-image" />
                    <button class="clear-preview" onclick={clearPreview}>
                        <X size={16} />
                    </button>
                </div>
            {/if}
        </div>
    </div>
</div>

<style lang="scss">
    .search-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 0 1rem;
    }

    .search-box {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    }

    .search-input-group {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .type-select {
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 0.9rem;
        background: white;
        color: #666;
        cursor: pointer;
        transition: all 0.3s ease;

        &:focus {
            outline: none;
            border-color: #dd2476;
            box-shadow: 0 0 0 2px rgba(221, 36, 118, 0.1);
        }
    }

    input {
        flex: 1;
        padding: 0.75rem 1rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 0.9rem;
        background: white;
        transition: all 0.3s ease;

        &:focus {
            outline: none;
            border-color: #dd2476;
            box-shadow: 0 0 0 2px rgba(221, 36, 118, 0.1);
        }
    }

    .search-btn {
        padding: 0.75rem 1.5rem;
        background: linear-gradient(45deg, #ff512f, #dd2476);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
        transition: transform 0.2s;

        &:hover {
            transform: translateY(-1px);
        }
    }

    .divider {
        margin: 1.25rem 0;
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        position: relative;

        &::before,
        &::after {
            content: "";
            position: absolute;
            top: 50%;
            width: 45%;
            height: 1px;
            background: #ddd;
        }

        &::before {
            left: 0;
        }

        &::after {
            right: 0;
        }
    }

    .upload-btn {
        width: 100%;
        padding: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        background: white;
        border: 1px dashed #ddd;
        border-radius: 8px;
        color: #666;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
            border-color: #dd2476;
            color: #dd2476;
            background: rgba(221, 36, 118, 0.05);
        }
    }
/* 修改預覽相關樣式 */
.preview-container {
        margin-top: 1rem;
        position: relative;
        width: 200px; /* 設定固定寬度 */
        margin-left: auto;
        margin-right: auto;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #ddd;
    }

    .preview-image {
        width: 100%;
        height: 200px; /* 設定固定高度 */
        display: block;
        border-radius: 8px;
        object-fit: cover; /* 確保圖片填滿容器且不變形 */
    }

    .clear-preview {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: rgba(0, 0, 0, 0.5);
        border: none;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: white;
        padding: 0;
        transition: background-color 0.2s;

        &:hover {
            background: rgba(0, 0, 0, 0.7);
        }
    }

    @media (max-width: 480px) {
        .search-input-group {
            flex-direction: column;

            .type-select,
            input,
            .search-btn {
                width: 100%;
            }
        }

        .preview-container {
            width: 150px; /* 手機版更小的預覽圖 */
        }

        .preview-image {
            height: 150px;
        }
    }
</style>
