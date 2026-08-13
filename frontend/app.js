/*
Project : URL Shortener API
Project ID : 018

Frontend Application Logic
*/


// ============================================================
// API CONFIGURATION
// ============================================================

const API_BASE_URL = "http://localhost:8000";


// ============================================================
// URL CREATION ELEMENTS
// ============================================================

const urlForm =
    document.getElementById("url-form");

const originalUrlInput =
    document.getElementById("original-url");

const customAliasInput =
    document.getElementById("custom-alias");

const expiresAtInput =
    document.getElementById("expires-at");

const shortenButton =
    document.getElementById("shorten-button");


// ============================================================
// MESSAGE
// ============================================================

const message =
    document.getElementById("message");


// ============================================================
// CREATED SHORT URL
// ============================================================

const resultSection =
    document.getElementById("result-section");

const shortUrlInput =
    document.getElementById("short-url");

const copyButton =
    document.getElementById("copy-button");


// ============================================================
// ANALYTICS LOOKUP
// ============================================================

const analyticsUrlInput =
    document.getElementById("analytics-url");

const analyticsCopyButton =
    document.getElementById(
        "analytics-copy-button"
    );

const getAnalyticsButton =
    document.getElementById(
        "get-analytics-button"
    );


// ============================================================
// ANALYTICS RESULTS
// ============================================================

const analyticsSection =
    document.getElementById(
        "analytics-section"
    );

const analyticsShortUrl =
    document.getElementById(
        "analytics-short-url"
    );

const totalClicks =
    document.getElementById(
        "total-clicks"
    );

const firstClickedAt =
    document.getElementById(
        "first-clicked-at"
    );

const lastClickedAt =
    document.getElementById(
        "last-clicked-at"
    );

const refreshAnalyticsButton =
    document.getElementById(
        "refresh-analytics-button"
    );


// ============================================================
// ANALYTICS STATE
// ============================================================

let currentAnalyticsIdentifier = null;


// ============================================================
// MESSAGE FUNCTIONS
// ============================================================

function showMessage(text, type) {

    message.textContent = text;

    message.className =
        `message ${type}`;

    message.hidden = false;
}


function hideMessage() {

    message.textContent = "";

    message.className = "message";

    message.hidden = true;
}


// ============================================================
// RESULT FUNCTIONS
// ============================================================

function showResult(shortUrl) {

    shortUrlInput.value =
        shortUrl;

    resultSection.hidden =
        false;
}


function hideResult() {

    shortUrlInput.value = "";

    resultSection.hidden =
        true;
}


// ============================================================
// BUILD CREATE URL REQUEST
// ============================================================

function buildRequestPayload() {

    const payload = {
        original_url:
            originalUrlInput.value.trim(),
    };


    const customAlias =
        customAliasInput.value.trim();


    if (customAlias) {

        payload.custom_alias =
            customAlias;
    }


    const expiresAt =
        expiresAtInput.value;


    if (expiresAt) {

        payload.expires_at =
            new Date(
                expiresAt
            ).toISOString();
    }


    return payload;
}


// ============================================================
// CREATE SHORT URL API
// ============================================================

async function createShortUrl(payload) {

    const response =
        await fetch(
            `${API_BASE_URL}/api/v1/urls`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Accept":
                        "application/json",
                },

                body:
                    JSON.stringify(payload),
            }
        );


    let data = null;


    try {

        data =
            await response.json();

    } catch {

        data = null;
    }


    if (!response.ok) {

        let detail =
            "Unable to create the shortened URL.";


        if (data?.detail) {

            if (
                typeof data.detail ===
                "string"
            ) {

                detail =
                    data.detail;

            } else {

                detail =
                    JSON.stringify(
                        data.detail
                    );
            }
        }


        throw new Error(detail);
    }


    return data;
}


// ============================================================
// EXTRACT SHORT CODE / CUSTOM ALIAS
// ============================================================

function extractIdentifier(value) {

    const input =
        value.trim();


    if (!input) {

        throw new Error(
            "Please enter a short URL."
        );
    }


    /*
     * User can enter either:
     *
     * http://localhost:8000/my-company
     *
     * or:
     *
     * my-company
     */

    try {

        const parsedUrl =
            new URL(input);


        const path =
            parsedUrl.pathname
                .replace(
                    /^\/+|\/+$/g,
                    ""
                );


        if (!path) {

            throw new Error(
                "Please enter a valid short URL."
            );
        }


        return path.split("/").pop();

    } catch {

        /*
         * If it isn't a complete URL,
         * treat it as an identifier.
         */

        const identifier =
            input
                .replace(
                    /^\/+|\/+$/g,
                    ""
                )
                .split("/")
                .pop();


        if (!identifier) {

            throw new Error(
                "Please enter a valid short URL."
            );
        }


        return identifier;
    }
}


// ============================================================
// ANALYTICS API
// ============================================================

async function loadAnalytics(identifier) {

    const response =
        await fetch(
            `${API_BASE_URL}/api/v1/analytics/${encodeURIComponent(identifier)}`,
            {
                method: "GET",

                headers: {
                    "Accept":
                        "application/json",
                },
            }
        );


    let data = null;


    try {

        data =
            await response.json();

    } catch {

        data = null;
    }


    if (!response.ok) {

        let detail =
            "Unable to load URL analytics.";


        /*
         * Important:
         *
         * FastAPI can return detail as either:
         *
         * "Some error"
         *
         * or an object/list.
         *
         * JSON.stringify prevents:
         *
         * [object Object]
         */

        if (data?.detail) {

            if (
                typeof data.detail ===
                "string"
            ) {

                detail =
                    data.detail;

            } else {

                detail =
                    JSON.stringify(
                        data.detail
                    );
            }
        }


        throw new Error(detail);
    }


    return data;
}


// ============================================================
// FORMAT TIMESTAMP
// ============================================================

function formatTimestamp(timestamp) {

    if (!timestamp) {

        return "-";
    }


    const date =
        new Date(timestamp);


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return String(timestamp);
    }


    return date.toLocaleString();
}


// ============================================================
// DISPLAY ANALYTICS
// ============================================================

function showAnalytics(
    data,
    shortUrl
) {

    analyticsShortUrl.textContent =
        shortUrl;


    totalClicks.textContent =
        data.total_clicks ??
        0;


    firstClickedAt.textContent =
        formatTimestamp(
            data.first_clicked_at
        );


    lastClickedAt.textContent =
        formatTimestamp(
            data.last_clicked_at
        );


    analyticsSection.hidden =
        false;
}


// ============================================================
// GET ANALYTICS
// ============================================================

async function getAnalytics() {

    const input =
        analyticsUrlInput.value.trim();


    try {

        const identifier =
            extractIdentifier(input);


        /*
         * Store only the identifier being
         * analysed.
         *
         * This is completely independent
         * of URL creation.
         */

        currentAnalyticsIdentifier =
            identifier;


        getAnalyticsButton.disabled =
            true;

        getAnalyticsButton.textContent =
            "Loading...";


        const analytics =
            await loadAnalytics(
                identifier
            );


        showAnalytics(
            analytics,
            input
        );


        showMessage(
            "Analytics loaded successfully.",
            "success"
        );

    } catch (error) {

        analyticsSection.hidden =
            true;


        showMessage(
            error.message ||
                "Unable to load analytics.",
            "error"
        );

    } finally {

        getAnalyticsButton.disabled =
            false;

        getAnalyticsButton.textContent =
            "Get Analytics";
    }
}


// ============================================================
// REFRESH ANALYTICS
// ============================================================

async function refreshAnalytics() {

    if (!currentAnalyticsIdentifier) {

        showMessage(
            "Enter a short URL and click Get Analytics first.",
            "error"
        );

        return;
    }


    refreshAnalyticsButton.disabled =
        true;

    refreshAnalyticsButton.textContent =
        "Refreshing...";


    try {

        const analytics =
            await loadAnalytics(
                currentAnalyticsIdentifier
            );


        showAnalytics(
            analytics,
            analyticsUrlInput.value.trim()
        );


        showMessage(
            "Analytics refreshed successfully.",
            "success"
        );

    } catch (error) {

        showMessage(
            error.message ||
                "Unable to refresh analytics.",
            "error"
        );

    } finally {

        refreshAnalyticsButton.disabled =
            false;

        refreshAnalyticsButton.textContent =
            "Refresh";
    }
}


// ============================================================
// COPY CREATED SHORT URL
// ============================================================

copyButton.addEventListener(
    "click",
    async () => {

        const shortUrl =
            shortUrlInput.value;


        if (!shortUrl) {

            return;
        }


        try {

            await navigator.clipboard.writeText(
                shortUrl
            );


            showMessage(
                "Short URL copied to clipboard.",
                "success"
            );

        } catch {

            shortUrlInput.select();

            document.execCommand(
                "copy"
            );


            showMessage(
                "Short URL copied to clipboard.",
                "success"
            );
        }
    }
);


// ============================================================
// COPY ANALYTICS URL
// ============================================================

analyticsCopyButton.addEventListener(
    "click",
    async () => {

        const analyticsUrl =
            analyticsUrlInput.value.trim();


        if (!analyticsUrl) {

            return;
        }


        try {

            await navigator.clipboard.writeText(
                analyticsUrl
            );


            showMessage(
                "URL copied to clipboard.",
                "success"
            );

        } catch {

            analyticsUrlInput.select();

            document.execCommand(
                "copy"
            );


            showMessage(
                "URL copied to clipboard.",
                "success"
            );
        }
    }
);


// ============================================================
// CREATE URL FORM
// ============================================================

urlForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        hideMessage();

        hideResult();


        shortenButton.disabled =
            true;

        shortenButton.textContent =
            "Creating...";


        try {

            const payload =
                buildRequestPayload();


            const result =
                await createShortUrl(
                    payload
                );


            /*
             * URL creation is independent
             * of analytics.
             */

            showResult(
                result.short_url
            );


            /*
             * Convenience:
             * populate analytics input with
             * the newly created short URL.
             *
             * The user can replace it with
             * ANY existing URL.
             */

            analyticsUrlInput.value =
                result.short_url;


            showMessage(
                "Short URL created successfully.",
                "success"
            );

        } catch (error) {

            showMessage(
                error.message ||
                    "An unexpected error occurred.",
                "error"
            );

        } finally {

            shortenButton.disabled =
                false;

            shortenButton.textContent =
                "Shorten URL";
        }
    }
);


// ============================================================
// GET ANALYTICS BUTTON
// ============================================================

getAnalyticsButton.addEventListener(
    "click",
    async () => {

        await getAnalytics();
    }
);


// ============================================================
// REFRESH ANALYTICS BUTTON
// ============================================================

refreshAnalyticsButton.addEventListener(
    "click",
    async () => {

        await refreshAnalytics();
    }
);