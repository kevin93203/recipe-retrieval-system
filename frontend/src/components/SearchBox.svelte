<script lang="ts">
    import { Camera, X } from "lucide-svelte";

    let { handleSearch, handleImageUpload } = $props();
    import { searchState } from "../routes/shared.svelte";

    let fileInput: HTMLInputElement = $state();

    function handleSubmit() {
        if (searchState.selectedFile) {
            handleImageUpload(searchState.selectedFile, searchState.imageSearchTerm);
        } else {
            handleSearch(searchState.searchInput);
        }
    }

    function handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            searchState.selectedFile = file;
            searchState.previewUrl = URL.createObjectURL(file);
        }
        event.target.value = "";
    }

    function handleTypeChange(e: Event) {
        const select = e.target as HTMLSelectElement;
        searchState.type = select.value;
        searchState.searchInput = "";
        clearImageSearch();
    }

    function clearImageSearch() {
        searchState.searchInput = "";
        searchState.selectedFile = null;
        searchState.previewUrl = "";
        searchState.imageSearchTerm = "";
        if (searchState.previewUrl) {
            URL.revokeObjectURL(searchState.previewUrl);
        }
    }
</script>

<div class="search-container">
    <div class="search-box">
        <div class="search-input-group">
            {#if !searchState.selectedFile}
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
                    bind:value={searchState.searchInput}
                    placeholder={searchState.type === "recipe"
                        ? "輸入食譜名稱..."
                        : "輸入食材名稱..."}
                    onkeyup={(e) => e.key === "Enter" && handleSubmit()}
                />
            {:else}
                <div class="image-search-input">
                    {#if searchState.previewUrl}
                        <div class="preview-container">
                            <img src={searchState.previewUrl} alt="Preview" class="preview-image" />
                        </div>
                    {/if}
                    <input
                        type="text"
                        bind:value={searchState.imageSearchTerm}
                        placeholder="輸入額外的搜尋條件..."
                        onkeyup={(e) => e.key === "Enter" && handleSubmit()}
                    />
                    <button class="clear-preview" onclick={clearImageSearch}>
                        <X size={16} />
                    </button>
                </div>
            {/if}
            
            <button class="search-btn" onclick={handleSubmit}>
                搜尋
            </button>
        </div>

        {#if !searchState.selectedFile}
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
            </div>
        {/if}
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

    .image-search-input {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 0.25rem;
        position: relative;

        input {
            flex: 1;
            border: none;
            padding: 0.5rem;
            font-size: 0.9rem;
            
            &:focus {
                outline: none;
            }
        }

        &:focus-within {
            border-color: #dd2476;
            box-shadow: 0 0 0 2px rgba(221, 36, 118, 0.1);
        }
    }

    .preview-container {
        width: 40px;
        height: 40px;
        border-radius: 4px;
        overflow: hidden;
    }

    .preview-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    input:not(.image-search-input input) {
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

    .clear-preview {
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        border-radius: 50%;
        background: #f0f0f0;
        color: #666;
        cursor: pointer;
        transition: all 0.2s;

        &:hover {
            background: #e0e0e0;
            color: #333;
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

    @media (max-width: 480px) {
        .search-input-group {
            flex-direction: column;

            .type-select,
            input,
            .image-search-input,
            .search-btn {
                width: 100%;
            }
        }
    }
</style>